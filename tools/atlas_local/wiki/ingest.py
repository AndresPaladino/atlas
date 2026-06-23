"""Estado de ingestión raw→wiki.

Hay dos perspectivas complementarias:

* ``raw_ingest_status`` — arranca desde ``raw/.atlas-extract.json`` (el Manifest
  de extracción) y pregunta: ¿qué PDFs existen en raw/ y cuánto de cada uno ya
  está cubierto por páginas en wiki/sources/?  Es la vista de inventario: muestra
  pending / partial / ingested para *cada fuente*, incluso las que nunca tuvieron
  una page en la wiki.

* ``source_status`` / ``ingest_status`` — arranca desde wiki/sources/ y pregunta:
  para cada page ya creada, ¿el raw que la originó cambió?  Es la vista de
  frescura: new / stale / current / missing-raw.  La usa ``ingest-stamp`` y el
  flujo --compile para saltear re-ingestas.

Las dos vistas son complementarias: la primera descubre huecos, la segunda detecta
drift en lo que ya existe.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from ..manifest import Manifest, sha256_file
from .loader import Page

_HASH_LINE = re.compile(r"^ingested_sha256:.*\n", re.MULTILINE)

# Carpetas cuyas páginas declaran cobertura de un raw (path:/chunks:/ingested_sha256):
# sources (material de estudio) y assessments (exámenes). Ambas se ingieren desde raw/.
_INGESTABLE_FOLDERS = ("sources", "assessments")


# ── vista de frescura (wiki/sources/ → raw/) ─────────────────────────────────

@dataclass
class SourceStatus:
    slug: str
    status: str            # new | stale | current | missing-raw
    raw_path: str | None   # rel al repo, el archivo cuyo hash se compara

    def as_dict(self) -> dict:
        return {"slug": self.slug, "status": self.status, "raw_path": self.raw_path}


def _raw_file(repo_root: Path, page: Page) -> Path | None:
    """Archivo raw cuyo cambio define si hay que re-ingerir.

    Para sources con chunks: prefiere el primer chunk listado en ``chunks``
    (frontmatter), o cae al campo ``extracted`` (puede ser el .md monolítico
    legacy), o al ``path`` (el .pdf).
    """
    fm = page.frontmatter
    # chunks lista explícita → usamos el primero como proxy de frescura del raw
    chunks = fm.get("chunks") or []
    if chunks:
        p = repo_root / str(chunks[0])
        if p.exists():
            return p
    candidates = [fm.get(k) for k in ("extracted", "path")]
    candidates = [repo_root / str(v) for v in candidates if v]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0] if candidates else None


def source_status(repo_root: Path, page: Page) -> SourceStatus:
    raw = _raw_file(repo_root, page)
    rel = raw.relative_to(repo_root).as_posix() if raw else None
    if raw is None or not raw.exists():
        return SourceStatus(page.slug, "missing-raw", rel)
    recorded = page.frontmatter.get("ingested_sha256")
    if not isinstance(recorded, str) or len(recorded) != 64:
        return SourceStatus(page.slug, "new", rel)
    status = "current" if sha256_file(raw) == recorded else "stale"
    return SourceStatus(page.slug, status, rel)


def ingest_status(pages: list[Page], repo_root: Path) -> list[SourceStatus]:
    """Vista de frescura: estado de cada página ingerida desde raw/ (sources + assessments)."""
    return [source_status(repo_root, p) for p in pages if p.folder in _INGESTABLE_FOLDERS]


# ── vista de inventario (raw/.atlas-extract.json → wiki/sources/) ────────────

@dataclass
class RawStatus:
    """Estado de ingestión de un PDF visto desde raw/."""
    pdf_key: str           # rel a raw/, ej. "DDSE.pdf"
    status: str            # pending | partial | ingested
    n_chunks: int          # 0 si no hay carpeta de chunks
    covered_chunks: list[str] = field(default_factory=list)   # nombres de chunk cubiertos
    sources: list[str] = field(default_factory=list)          # slugs en wiki/sources/

    @property
    def uncovered_chunks_count(self) -> int:
        return max(0, self.n_chunks - len(self.covered_chunks))

    def as_dict(self) -> dict:
        return {
            "pdf_key": self.pdf_key,
            "status": self.status,
            "n_chunks": self.n_chunks,
            "covered_chunks": self.covered_chunks,
            "uncovered_chunks": self.uncovered_chunks_count,
            "sources": self.sources,
        }


def _chunks_covered_by(pages: list[Page], chunks_dir: str, repo_root: Path) -> dict[str, list[str]]:
    """Para cada chunk en chunks_dir, devuelve los slugs de sources que lo cubren.

    Busca en el frontmatter de cada source:
    - ``chunks``: lista de rutas relativas al repo (nueva convención)
    - ``extracted``: ruta única al .md (convención legacy — puede ser el monolítico
      o un chunk individual)

    Devuelve {chunk_filename: [slug, ...]}
    """
    covered: dict[str, list[str]] = {}
    chunks_prefix = chunks_dir.rstrip("/") + "/"   # ej. "extracted/DDSE/"

    for page in pages:
        if page.folder not in _INGESTABLE_FOLDERS:
            continue
        fm = page.frontmatter

        # nueva convención: chunks es lista de rutas
        chunk_list = fm.get("chunks") or []
        for c in chunk_list:
            c_str = str(c)
            if c_str.startswith(chunks_prefix):
                fname = c_str[len(chunks_prefix):]
                covered.setdefault(fname, []).append(page.slug)

        # legado: extracted apunta a un único archivo dentro de chunks_dir
        extracted = fm.get("extracted")
        if extracted:
            e_str = str(extracted)
            if e_str.startswith(chunks_prefix):
                fname = e_str[len(chunks_prefix):]
                covered.setdefault(fname, []).append(page.slug)

    return covered


def raw_ingest_status(pages: list[Page], raw_dir: Path, repo_root: Path, artifacts_dir: Path | None = None) -> list[RawStatus]:
    """Vista de inventario: estado de ingestión de cada PDF en raw/.

    Arranca desde el Manifest (raw/.atlas-extract.json) para conocer qué PDFs
    existen y qué artefactos produjeron.  Para cada PDF calcula:

    - pending   : ninguna source en wiki/ tiene path: apuntando a este PDF
    - partial   : hay sources pero no todos los chunks están cubiertos
    - ingested  : hay al menos una source (y si hay chunks, todos están cubiertos)
    """
    art_dir = artifacts_dir if artifacts_dir is not None else raw_dir
    manifest = Manifest.load(raw_dir, art_dir)

    # índice: path: "raw/X.pdf" → slugs de sources que lo declaran
    path_to_slugs: dict[str, list[str]] = {}
    for page in pages:
        if page.folder not in _INGESTABLE_FOLDERS:
            continue
        raw_path = page.frontmatter.get("path")
        if raw_path:
            path_to_slugs.setdefault(str(raw_path), []).append(page.slug)

    results: list[RawStatus] = []
    for pdf_key, entry in manifest._entries.items():
        # El manifest acumula entradas de extracciones pasadas; si el PDF ya no
        # está en raw/ es un fantasma (carpeta renombrada, fuente movida) y no
        # debe reportarse — si no, inunda la tabla de 'pending' espurios.
        if not (raw_dir / pdf_key).exists():
            continue
        slugs = path_to_slugs.get(f"raw/{pdf_key}", [])

        if not entry.chunks_dir:
            # PDF sin chunks: pending o ingested
            status = "ingested" if slugs else "pending"
            results.append(RawStatus(
                pdf_key=pdf_key,
                status=status,
                n_chunks=0,
                sources=slugs,
            ))
            continue

        # PDF con carpeta de chunks
        art_prefix = art_dir.relative_to(repo_root).as_posix()
        chunks_dir_rel = f"{art_prefix}/{entry.chunks_dir}"   # ej. "extracted/DDSE"
        chunks_dir_abs = art_dir / entry.chunks_dir
        all_chunks = sorted(
            p.name for p in chunks_dir_abs.iterdir()
            if p.is_file() and p.suffix == ".md"
        ) if chunks_dir_abs.exists() else []

        covered_map = _chunks_covered_by(pages, chunks_dir_rel, repo_root)
        covered = [c for c in all_chunks if c in covered_map]

        # Convención legacy: la fuente se ingirió como un único .md monolítico
        # (extracted: extracted/X.md) y el PDF se re-chunkeó *después*. El monolito
        # cubre todo el PDF aunque no enumere los chunks → no es 'partial' espurio.
        monolith_md = f"{art_prefix}/{entry.md_path}"
        monolith = any(
            str(p.frontmatter.get("extracted") or "") == monolith_md
            for p in pages if p.slug in slugs
        )

        if not slugs:
            status = "pending"
        elif monolith or (len(covered) >= len(all_chunks) and all_chunks):
            status = "ingested"
            if monolith and not covered:
                covered = all_chunks   # reflejar cobertura total en el conteo
        else:
            status = "partial"

        results.append(RawStatus(
            pdf_key=pdf_key,
            status=status,
            n_chunks=len(all_chunks),
            covered_chunks=covered,
            sources=slugs,
        ))

    return sorted(results, key=lambda r: (r.status != "pending", r.status != "partial", r.pdf_key))


# ── stamp ─────────────────────────────────────────────────────────────────────

def _insert_frontmatter_line(text: str, line: str) -> str:
    """Inserta ``line`` justo antes del ``---`` de cierre del frontmatter."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return line + text
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            lines.insert(i, line)
            return "".join(lines)
    return text


def _chunks_block(repo_root: Path, page: Page) -> str | None:
    """Bloque YAML ``chunks:`` con todos los .md del chunks_dir del raw de ``page``.

    None si la fuente no tiene path: con carpeta de chunks en el Manifest, o si
    el frontmatter ya declara ``chunks:`` (no pisamos lo que el ingestor puso).
    """
    fm = page.frontmatter
    if fm.get("chunks") or fm.get("extracted"):
        return None
    raw_path = fm.get("path")
    if not raw_path:
        return None
    pdf_key = str(raw_path)[len("raw/"):] if str(raw_path).startswith("raw/") else str(raw_path)
    raw_dir = repo_root / "raw"
    artifacts_dir = repo_root / "extracted"
    art_dir = artifacts_dir if artifacts_dir.is_dir() else raw_dir
    entry = Manifest.load(raw_dir, art_dir)._entries.get(pdf_key)
    if entry is None or not entry.chunks_dir:
        return None
    chunks_abs = art_dir / entry.chunks_dir
    names = sorted(
        p.name for p in chunks_abs.iterdir() if p.is_file() and p.suffix == ".md"
    ) if chunks_abs.exists() else []
    if not names:
        return None
    art_prefix = art_dir.relative_to(repo_root).as_posix()
    lines = ["chunks:\n"] + [f"  - {art_prefix}/{entry.chunks_dir}/{n}\n" for n in names]
    return "".join(lines)


def stamp_source(repo_root: Path, page: Page) -> str | None:
    """Sella ``ingested_sha256`` (y ``chunks:`` si falta) en el frontmatter. Devuelve el hash.

    None si no se encuentra el archivo raw a hashear.
    """
    raw = _raw_file(repo_root, page)
    if raw is None or not raw.exists():
        return None
    digest = sha256_file(raw)
    text = page.path.read_text(encoding="utf-8")
    line = f"ingested_sha256: {digest}\n"
    new = _HASH_LINE.sub(line, text, count=1) if _HASH_LINE.search(text) else _insert_frontmatter_line(text, line)
    chunks = _chunks_block(repo_root, page)
    if chunks:
        new = _insert_frontmatter_line(new, chunks)
    page.path.write_text(new, encoding="utf-8")
    return digest
