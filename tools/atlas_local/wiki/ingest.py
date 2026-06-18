"""Estado de ingestión raw→wiki: saltear fuentes ya ingeridas sin cambios.

Atlas ya hashea en la *extracción* (PDF→md, ver ``manifest.py``). Esto es el
paralelo en la *ingestión* (raw→wiki): el hash del archivo raw que se ingirió se
guarda en el frontmatter de la página de fuente como ``ingested_sha256:`` —
git-tracked y visible, igual que el resto del estado de Atlas.

``ingest_status`` compara ese hash con el archivo raw actual. ``/ingest
--compile`` saltea las fuentes ``current`` (cero llamadas LLM redundantes);
``stamp_source`` lo sella tras ingerir. Cálculo puro + escritura aislada.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from ..manifest import sha256_file
from .loader import Page

_HASH_LINE = re.compile(r"^ingested_sha256:.*\n", re.MULTILINE)


@dataclass
class SourceStatus:
    slug: str
    status: str            # new | stale | current | missing-raw
    raw_path: str | None   # rel al repo, el archivo cuyo hash se compara

    def as_dict(self) -> dict:
        return {"slug": self.slug, "status": self.status, "raw_path": self.raw_path}


def _raw_file(repo_root: Path, page: Page) -> Path | None:
    """Archivo raw cuyo cambio define si hay que re-ingerir.

    Prefiere ``extracted`` (el .md, lo que realmente lee el ingest y está
    versionado); cae a ``path`` (el .pdf, puede no estar en esta máquina).
    """
    candidates = [page.frontmatter.get(k) for k in ("extracted", "path")]
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
    if not recorded:
        return SourceStatus(page.slug, "new", rel)
    status = "current" if sha256_file(raw) == recorded else "stale"
    return SourceStatus(page.slug, status, rel)


def ingest_status(pages: list[Page], repo_root: Path) -> list[SourceStatus]:
    """Estado de ingestión de cada página de ``wiki/sources/``."""
    return [source_status(repo_root, p) for p in pages if p.folder == "sources"]


def _insert_frontmatter_line(text: str, line: str) -> str:
    """Inserta ``line`` justo antes del ``---`` de cierre del frontmatter."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return line + text  # sin frontmatter (no debería pasar en una source)
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            lines.insert(i, line)
            return "".join(lines)
    return text


def stamp_source(repo_root: Path, page: Page) -> str | None:
    """Sella ``ingested_sha256`` en el frontmatter de la fuente. Devuelve el hash.

    None si no se encuentra el archivo raw a hashear.
    """
    raw = _raw_file(repo_root, page)
    if raw is None or not raw.exists():
        return None
    digest = sha256_file(raw)
    text = page.path.read_text(encoding="utf-8")
    line = f"ingested_sha256: {digest}\n"
    new = _HASH_LINE.sub(line, text, count=1) if _HASH_LINE.search(text) else _insert_frontmatter_line(text, line)
    page.path.write_text(new, encoding="utf-8")
    return digest
