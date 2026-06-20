"""Carga del wiki: ``wiki/**/*.md`` → lista de :class:`Page`.

Una ``Page`` trae el frontmatter parseado, el cuerpo, los wikilinks del cuerpo
(con número de línea, para reportar) y las aristas declaradas en el frontmatter
(``requires`` / ``unlocks`` / ``sources`` / ``illustrates`` / ``covers_*``).

Es la base reutilizable de ``validate``, ``lint`` e ``index``. No depende de
nada pesado: solo ``pyyaml`` y la stdlib.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# Carpetas del wiki que contienen páginas con frontmatter (excluye index/log/README).
PAGE_DIRS = (
    "concepts",
    "theorems",
    "methods",
    "examples",
    "comparisons",
    "sources",
    "areas",
)

# Wikilink: [[slug]], [[carpeta/slug]] o [[slug|alias]]. Capturamos el target.
_WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def normalize_slug(target: str) -> str:
    """``[[folder/slug|alias]]`` → ``slug``. Tolera espacios, carpeta y alias."""
    target = target.strip()
    if "|" in target:
        target = target.split("|", 1)[0]
    if "/" in target:
        target = target.rsplit("/", 1)[-1]
    return target.strip()


@dataclass(frozen=True)
class Link:
    """Una referencia ``[[target]]`` encontrada en el cuerpo de una página."""

    target: str   # slug normalizado (sin carpeta ni alias)
    line: int     # número de línea 1-based dentro del archivo


@dataclass
class Page:
    """Una página del wiki ya parseada."""

    path: Path                     # ruta absoluta
    rel_path: str                  # ruta relativa al repo, posix ("wiki/concepts/x.md")
    slug: str                      # nombre de archivo sin .md
    folder: str                    # carpeta inmediata ("concepts", "theorems", ...)
    frontmatter: dict              # YAML parseado ({} si no hay o está roto)
    fm_error: str | None           # mensaje si el YAML no parseó
    body: str                      # cuerpo markdown (sin frontmatter)
    body_offset: int               # línea (1-based) donde arranca el cuerpo
    links: list[Link] = field(default_factory=list)  # wikilinks del cuerpo

    # ── accesos cómodos al frontmatter ───────────────────────────────────────
    @property
    def type(self) -> str | None:
        return self.frontmatter.get("type")

    @property
    def areas(self) -> list[str]:
        val = self.frontmatter.get("areas") or []
        return list(val) if isinstance(val, list) else [val]

    @property
    def aliases(self) -> list[str]:
        val = self.frontmatter.get("aliases") or []
        return list(val) if isinstance(val, list) else [val]

    @property
    def tags(self) -> list[str]:
        val = self.frontmatter.get("tags") or []
        return list(val) if isinstance(val, list) else [val]

    def edge(self, key: str) -> list[str]:
        """Slugs normalizados de una arista de frontmatter (requires/unlocks/...)."""
        raw = self.frontmatter.get(key) or []
        if not isinstance(raw, list):
            raw = [raw]
        out: list[str] = []
        for item in raw:
            for m in _WIKILINK.finditer(str(item)):
                out.append(normalize_slug(m.group(1)))
        return out


def split_frontmatter(text: str) -> tuple[dict, str | None, str, int]:
    """``text`` → (frontmatter, error, body, body_offset_línea_1based).

    Si no hay bloque ``---`` al inicio, frontmatter = {} y el cuerpo es todo.
    Si el YAML no parsea, error trae el mensaje (frontmatter queda {}).
    """
    if not text.startswith("---"):
        return {}, None, text, 1

    lines = text.splitlines(keepends=True)
    # Buscar el cierre del bloque (segundo "---" en su propia línea).
    end = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            end = i
            break
    if end is None:
        return {}, "frontmatter sin cierre '---'", text, 1

    raw_yaml = "".join(lines[1:end])
    body = "".join(lines[end + 1:])
    body_offset = end + 2  # 1-based: línea siguiente al cierre
    try:
        fm = yaml.safe_load(raw_yaml) or {}
        if not isinstance(fm, dict):
            return {}, "frontmatter no es un mapping YAML", body, body_offset
    except yaml.YAMLError as exc:
        return {}, f"YAML inválido: {exc}", body, body_offset
    return fm, None, body, body_offset


def _extract_links(body: str, body_offset: int) -> list[Link]:
    links: list[Link] = []
    for rel_line, text in enumerate(body.splitlines()):
        for m in _WIKILINK.finditer(text):
            links.append(Link(target=normalize_slug(m.group(1)),
                              line=body_offset + rel_line))
    return links


def load_page(path: Path, repo_root: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    fm, err, body, offset = split_frontmatter(text)
    return Page(
        path=path,
        rel_path=path.relative_to(repo_root).as_posix(),
        slug=path.stem,
        folder=path.parent.name,
        frontmatter=fm,
        fm_error=err,
        body=body,
        body_offset=offset,
        links=_extract_links(body, offset),
    )


def load_wiki(wiki_dir: Path, scope: str | None = None) -> list[Page]:
    """Carga todas las páginas del wiki.

    ``scope`` opcional: nombre de carpeta ("concepts") o área. Si es una carpeta
    existente, limita a ella; si no, se interpreta como filtro de área (se aplica
    tras cargar). El llamador decide el filtro de área para no acoplar el loader.
    """
    repo_root = wiki_dir.parent
    pages: list[Page] = []
    dirs = (scope,) if scope in PAGE_DIRS else PAGE_DIRS
    for sub in dirs:
        d = wiki_dir / sub
        if not d.is_dir():
            continue
        for md in sorted(d.glob("*.md")):
            pages.append(load_page(md, repo_root))
    return pages


def index_by_slug(pages: list[Page]) -> dict[str, Page]:
    """Mapa slug → Page. Si hay slugs duplicados en distintas carpetas, gana
    el último cargado; el lint reporta la colisión por separado si hace falta."""
    return {p.slug: p for p in pages}


def all_aliases(pages: list[Page]) -> dict[str, Page]:
    """Mapa alias/slug (lowercase) → Page, para resolver links y matchear T."""
    out: dict[str, Page] = {}
    for p in pages:
        out[p.slug.lower()] = p
        for a in p.aliases:
            out[str(a).strip().lower()] = p
    return out
