"""Extracción PDF → markdown.

Backend primario: **marker** (preserva LaTeX, extrae figuras), sobre el device
detectado (cuda/mps/cpu) vía torch. Fallback: **markitdown** (texto plano, sin
figuras) para el tier CPU o cuando marker no está disponible.

Los imports pesados son perezosos: importar este módulo no arrastra torch/marker,
así `doctor` y `status` corren en cualquier entorno.
"""

from __future__ import annotations

import io
import os
import re
import tempfile
from dataclasses import dataclass, field
from importlib import metadata
from pathlib import Path

from .config import CAPTION_MODEL, Tier
from .device import Device

# Backend LLM para --usellm: reusa Ollama (mismo modelo de --captions), sin API
# key ni dependencia de un servicio pago. marker soporta pasar la instancia de
# servicio ya configurada en artifact_dict, en vez de solo la ruta de clase.
_LLM_SERVICE_PATH = "marker.services.ollama.OllamaService"

# Por encima de este nº de páginas, marker procesa el doc por lotes (slices) para
# acotar el pico de memoria. Un escaneo de cientos de páginas, cargado entero,
# dispara el OOM killer del kernel ("Killed" sin traceback).
DEFAULT_BATCH_PAGES = 40

# Separador de página que emite marker con paginate_output: "{N}-----".
_PAGE_MARKER_RE = re.compile(r"^\{(\d+)\}(-{3,}.*)$", re.M)
# Nombre de imagen extraída por marker: _page_<N>_<Kind>_<idx>. N es 0-indexado.
_IMG_NAME_RE = re.compile(r"_page_(\d+)_([A-Za-z]+)_(\d+)")


def _offset_page_numbers(markdown: str, offset: int) -> str:
    """Reescribe los nº de página (separadores y refs de imagen) sumando offset.

    Cada slice arranca su numeración en 0; al concatenar lotes hay que llevarlos
    a la numeración global del documento para que la segmentación mapee bien las
    secciones a sus páginas.
    """
    if offset == 0:
        return markdown
    markdown = _PAGE_MARKER_RE.sub(
        lambda m: f"{{{int(m.group(1)) + offset}}}{m.group(2)}", markdown
    )
    markdown = _IMG_NAME_RE.sub(
        lambda m: f"_page_{int(m.group(1)) + offset}_{m.group(2)}_{m.group(3)}",
        markdown,
    )
    return markdown


def _offset_image_names(images: dict[str, bytes], offset: int) -> dict[str, bytes]:
    """Renombra las claves de imagen al espacio de páginas global (evita colisiones)."""
    if offset == 0:
        return images
    return {
        _IMG_NAME_RE.sub(
            lambda m: f"_page_{int(m.group(1)) + offset}_{m.group(2)}_{m.group(3)}",
            name,
        ): data
        for name, data in images.items()
    }


@dataclass
class ExtractResult:
    markdown: str
    extractor: str
    extractor_version: str
    n_pages: int = 0
    images: dict[str, bytes] = field(default_factory=dict)  # nombre → PNG bytes

    @property
    def n_figs(self) -> int:
        return len(self.images)


# ── checkpoint de lotes (resumable batches) ──────────────────────────────────
# Cada lote de la extracción batched se persiste apenas se procesa, en numeración
# global ya aplicada. Una corrida cortada a la mitad reanuda desde el primer lote
# faltante en vez de re-extraer el PDF entero. El chunking sigue siendo un paso
# final barato sobre el .md reensamblado (no se persiste por chunk: el chunking
# presupone el documento completo).
_BATCH_NAME_RE = re.compile(r"^p(\d+)-p(\d+)\.md$")


def _batch_stem(start: int, end: int) -> str:
    """Nombre canónico de un lote: ``p{start}-p{end}`` con zero-pad para que
    el orden lexicográfico coincida con el numérico."""
    return f"p{start:05d}-p{end:05d}"


def _write_batch(
    partial_dir: Path, start: int, end: int, markdown: str, images: dict[str, bytes]
) -> None:
    """Persiste un lote (markdown global + sus imágenes) en ``partial_dir``.

    Escritura atómica del ``.md``: se escribe a ``.tmp`` y se renombra, así un
    corte a mitad de escritura no deja un lote truncado que luego se lea como
    válido. Las imágenes van antes que el ``.md`` — el ``.md`` es el marcador de
    completitud del lote (ver ``_read_batches``)."""
    partial_dir.mkdir(parents=True, exist_ok=True)
    stem = _batch_stem(start, end)
    for name, data in images.items():
        (partial_dir / name).write_bytes(data)
    md_path = partial_dir / f"{stem}.md"
    tmp = md_path.with_suffix(".md.tmp")
    tmp.write_text(markdown, encoding="utf-8")
    tmp.replace(md_path)


def _read_batches(partial_dir: Path) -> dict[tuple[int, int], str]:
    """Lee los lotes ya persistidos: ``{(start, end): markdown}``.

    Solo cuenta un lote como presente si su ``.md`` existe (el marcador de
    completitud); ``.tmp`` sueltos de un corte se ignoran. Vacío si no hay dir."""
    out: dict[tuple[int, int], str] = {}
    if not partial_dir.is_dir():
        return out
    for md in partial_dir.glob("p*.md"):
        m = _BATCH_NAME_RE.match(md.name)
        if not m:
            continue
        out[(int(m.group(1)), int(m.group(2)))] = md.read_text(encoding="utf-8")
    return out


def _read_batch_images(partial_dir: Path) -> dict[str, bytes]:
    """Junta las imágenes de todos los lotes persistidos (claves ya globales)."""
    imgs: dict[str, bytes] = {}
    if not partial_dir.is_dir():
        return imgs
    for img in partial_dir.iterdir():
        if img.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            imgs[img.name] = img.read_bytes()
    return imgs


def _pkg_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "unknown"


def _page_count(pdf: Path) -> int:
    """Cuenta de páginas vía pypdfium2 (dep transitiva de marker). 0 si falla."""
    try:
        import pypdfium2 as pdfium

        doc = pdfium.PdfDocument(str(pdf))
        try:
            return len(doc)
        finally:
            doc.close()
    except Exception:
        return 0


def _png_bytes(image) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


class Extractor:
    """Convierte PDFs según el tier. Carga modelos de marker una sola vez (batch)."""

    def __init__(
        self,
        tier: Tier,
        device: Device,
        cache_dir: "Path | None" = None,
        use_llm: bool = False,
    ):
        self.tier = tier
        self.device = device
        self.cache_dir = cache_dir
        self.use_llm = use_llm
        self._converter = None  # marker, perezoso

    # ── marker ────────────────────────────────────────────────────────────────
    def _marker(self):
        if self._converter is None:
            # marker lee el device de la env var TORCH_DEVICE.
            os.environ.setdefault("TORCH_DEVICE", self.device.kind)

            # Redirigir la caché de modelos HuggingFace y torch a cache_dir
            # para evitar llenar C:\Users\..\.cache en Windows (los modelos
            # de marker pesan ~8 GB y van ahí por defecto).
            if self.cache_dir is not None:
                cache_str = str(self.cache_dir)
                os.environ.setdefault("HF_HOME", cache_str)
                os.environ.setdefault("HUGGINGFACE_HUB_CACHE", str(self.cache_dir / "hub"))
                os.environ.setdefault("TORCH_HOME", str(self.cache_dir / "torch"))

            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict

            # pdftext_workers=1 desactiva ProcessPoolExecutor en pdftext.
            # fork() después de inicializar CUDA crashea el kernel de WSL2
            # (y es inestable en general con CUDA). Los propios scripts de
            # servidor de marker fijan este mismo valor por la misma razón.
            #
            # paginate_output inserta separadores de página ("{N}----…") en el
            # markdown; la segmentación los usa para mapear cada sección a su
            # rango de páginas en el TOC. Es inocuo para el render y el ingest.
            config = {"pdftext_workers": 1, "paginate_output": True}
            llm_service = None
            if self.use_llm:
                # use_llm mejora tablas/ecuaciones/reading-order pasando cada
                # bloque dudoso por un LLM. Sin llm_service explícito, marker
                # usaría Gemini (default_llm_service) y pediría GOOGLE_API_KEY;
                # acá forzamos Ollama para no depender de una API key paga.
                # ollama_model va en config: PdfConverter arma el service con
                # OllamaService(config=config), que asigna sus propios campos
                # anotados (ollama_model, ollama_base_url) desde ese dict.
                config["use_llm"] = True
                config["ollama_model"] = CAPTION_MODEL
                llm_service = _LLM_SERVICE_PATH

            self._converter = PdfConverter(
                artifact_dict=create_model_dict(),
                config=config,
                llm_service=llm_service,
            )
        return self._converter

    def _run_marker(self, pdf: Path) -> "tuple[str, dict[str, bytes]]":
        """Corre marker sobre un PDF y devuelve (markdown, imágenes PNG)."""
        from marker.output import text_from_rendered

        rendered = self._marker()(str(pdf))
        markdown, _ext, images = text_from_rendered(rendered)
        png = {name: _png_bytes(img) for name, img in (images or {}).items()}
        return markdown, png

    def _extract_marker(self, pdf: Path) -> ExtractResult:
        markdown, png = self._run_marker(pdf)
        return ExtractResult(
            markdown=markdown,
            extractor="marker",
            extractor_version=_pkg_version("marker-pdf"),
            n_pages=_page_count(pdf),
            images=png,
        )

    def _extract_marker_batched(
        self,
        pdf: Path,
        batch_pages: int,
        on_progress=None,
        partial_dir: "Path | None" = None,
    ) -> ExtractResult:
        """Extrae un PDF grande por lotes de páginas para acotar la memoria.

        Recorta el PDF en slices de ``batch_pages`` páginas (reusando pdfslice),
        corre marker en cada uno —los modelos quedan cargados una sola vez— y
        concatena el markdown reindexando páginas e imágenes a la numeración
        global. Salida idéntica a procesarlo entero, pero con pico acotado.

        Si se pasa ``partial_dir``, cada lote se persiste apenas se procesa y una
        corrida reanudada saltea los lotes ya en disco (checkpoint resumible). El
        caller es responsable de limpiar ``partial_dir`` cuando el PDF termina.
        """
        from .pdfslice import page_count, slice_pdf

        n_pages = page_count(pdf)
        done = _read_batches(partial_dir) if partial_dir is not None else {}
        parts: dict[tuple[int, int], str] = dict(done)
        images: dict[str, bytes] = (
            _read_batch_images(partial_dir) if partial_dir is not None else {}
        )

        with tempfile.TemporaryDirectory(prefix="atlas-slice-") as tmp:
            tmp_dir = Path(tmp)
            for start in range(1, n_pages + 1, batch_pages):
                end = min(start + batch_pages - 1, n_pages)
                if (start, end) in done:
                    continue  # lote ya persistido de una corrida previa
                if on_progress:
                    on_progress(start, end, n_pages)
                slice_path = tmp_dir / f"{pdf.stem}_p{start}-p{end}.pdf"
                slice_pdf(pdf, start, end, slice_path)
                try:
                    md, png = self._run_marker(slice_path)
                finally:
                    slice_path.unlink(missing_ok=True)
                offset = start - 1  # numeración de marker es 0-indexada
                md_global = _offset_page_numbers(md, offset)
                png_global = _offset_image_names(png, offset)
                if partial_dir is not None:
                    _write_batch(partial_dir, start, end, md_global, png_global)
                parts[(start, end)] = md_global
                images.update(png_global)

        ordered = [parts[k] for k in sorted(parts)]
        return ExtractResult(
            markdown="\n\n".join(ordered),
            extractor="marker",
            extractor_version=_pkg_version("marker-pdf"),
            n_pages=n_pages,
            images=images,
        )

    # ── markitdown (fallback) ───────────────────────────────────────────────────
    def _extract_markitdown(self, pdf: Path) -> ExtractResult:
        from markitdown import MarkItDown

        result = MarkItDown().convert(str(pdf))
        return ExtractResult(
            markdown=result.text_content or "",
            extractor="markitdown",
            extractor_version=_pkg_version("markitdown"),
            n_pages=_page_count(pdf),
            images={},
        )

    # ── dispatch ────────────────────────────────────────────────────────────────
    def extract(
        self,
        pdf: Path,
        batch_pages: int = 0,
        on_progress=None,
        partial_dir: "Path | None" = None,
    ) -> ExtractResult:
        if self.tier.extractor == "marker":
            try:
                if batch_pages > 0 and _page_count(pdf) > batch_pages:
                    return self._extract_marker_batched(
                        pdf, batch_pages, on_progress, partial_dir=partial_dir
                    )
                return self._extract_marker(pdf)
            except ImportError as exc:  # marker no instalado → degradar a texto plano
                raise RuntimeError(
                    "marker-pdf no está disponible; reinstalá con ./install.sh "
                    f"o forzá el fallback de texto. Detalle: {exc}"
                ) from exc
        return self._extract_markitdown(pdf)
