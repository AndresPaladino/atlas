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
from dataclasses import dataclass, field
from importlib import metadata
from pathlib import Path

from .config import Tier
from .device import Device


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

    def __init__(self, tier: Tier, device: Device):
        self.tier = tier
        self.device = device
        self._converter = None  # marker, perezoso

    # ── marker ────────────────────────────────────────────────────────────────
    def _marker(self):
        if self._converter is None:
            # marker lee el device de la env var TORCH_DEVICE.
            os.environ.setdefault("TORCH_DEVICE", self.device.kind)
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict

            # pdftext_workers=1 desactiva ProcessPoolExecutor en pdftext.
            # fork() después de inicializar CUDA crashea el kernel de WSL2
            # (y es inestable en general con CUDA). Los propios scripts de
            # servidor de marker fijan este mismo valor por la misma razón.
            self._converter = PdfConverter(
                artifact_dict=create_model_dict(),
                config={"pdftext_workers": 1},
            )
        return self._converter

    def _extract_marker(self, pdf: Path) -> ExtractResult:
        from marker.output import text_from_rendered

        rendered = self._marker()(str(pdf))
        markdown, _ext, images = text_from_rendered(rendered)
        png = {name: _png_bytes(img) for name, img in (images or {}).items()}
        return ExtractResult(
            markdown=markdown,
            extractor="marker",
            extractor_version=_pkg_version("marker-pdf"),
            n_pages=_page_count(pdf),
            images=png,
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
    def extract(self, pdf: Path) -> ExtractResult:
        if self.tier.extractor == "marker":
            try:
                return self._extract_marker(pdf)
            except ImportError as exc:  # marker no instalado → degradar a texto plano
                raise RuntimeError(
                    "marker-pdf no está disponible; reinstalá con ./install.sh "
                    f"o forzá el fallback de texto. Detalle: {exc}"
                ) from exc
        return self._extract_markitdown(pdf)
