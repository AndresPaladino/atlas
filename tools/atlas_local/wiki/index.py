"""Generación de ``wiki/index.md`` y ``wiki/areas/*.md`` desde el filesystem.

El catálogo deja de mantenerse a mano (y por lo tanto deja de driftar). Cada
archivo lleva un bloque Dataview (render en Obsidian) **y** una lista plana
generada entre marcadores ``<!-- atlas:auto … -->`` para clientes sin Dataview
y para que los modos LLM tengan un catálogo plano sin releer 56 archivos.

Solo se reescribe lo que está entre marcadores: el frontmatter, los títulos y
las descripciones humanas se preservan.
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from .loader import Page, load_wiki

_AUTO_START = "<!-- atlas:auto:start -->"
_AUTO_END = "<!-- atlas:auto:end -->"

_TYPE_SECTIONS = [
    ("concept", "Conceptos", "concepts"),
    ("theorem", "Teoremas", "theorems"),
    ("method", "Métodos", "methods"),
    ("example", "Ejemplos", "examples"),
    ("comparison", "Comparaciones", "comparisons"),
    ("source", "Fuentes", "sources"),
]

_AREAS = ["math", "signals", "computing", "engineering-physics", "ml"]


def _today() -> str:
    return _dt.date.today().isoformat()


def _replace_auto_block(text: str, new_block: str) -> str:
    """Reemplaza el contenido entre marcadores. Si faltan, los agrega al final."""
    block = f"{_AUTO_START}\n{new_block}\n{_AUTO_END}"
    if _AUTO_START in text and _AUTO_END in text:
        return re.sub(
            re.escape(_AUTO_START) + r".*?" + re.escape(_AUTO_END),
            lambda _: block, text, count=1, flags=re.DOTALL,
        )
    return text.rstrip() + "\n\n" + block + "\n"


def _bump_updated(text: str) -> str:
    if re.search(r"^updated:.*$", text, flags=re.MULTILINE):
        return re.sub(r"^updated:.*$", f"updated: {_today()}", text,
                      count=1, flags=re.MULTILINE)
    return text


def _list_links(pages: list[Page]) -> str:
    if not pages:
        return "_(ninguna todavía)_"
    return "\n".join(f"- [[{p.slug}]]" for p in sorted(pages, key=lambda p: p.slug))


# ── index.md ──────────────────────────────────────────────────────────────────
def render_index(pages: list[Page]) -> str:
    by_type: dict[str, list[Page]] = {t: [] for t, _, _ in _TYPE_SECTIONS}
    for p in pages:
        if p.type in by_type:
            by_type[p.type].append(p)

    out: list[str] = [
        f"---\ntype: index\nupdated: {_today()}\n---",
        "",
        "# Wiki — catálogo",
        "",
        "> **Generado por `atlas index`.** No editar a mano la zona entre "
        "marcadores. Los bloques Dataview se renderizan en Obsidian; la lista "
        "plana de abajo es la fuente para clientes sin Dataview y para los modos.",
        "",
        _AUTO_START,
    ]
    for ptype, title, folder in _TYPE_SECTIONS:
        out += [
            "",
            f"## {title}",
            "",
            "```dataview",
            f"TABLE areas FROM \"wiki/{folder}\" SORT file.name ASC",
            "```",
            "",
            _list_links(by_type[ptype]),
        ]
    out += [
        "",
        "## Áreas (MOCs)",
        "",
        *[f"- [[areas/{a}]]" for a in _AREAS],
        "",
        _AUTO_END,
        "",
    ]
    return "\n".join(out)


# ── areas/<area>.md ───────────────────────────────────────────────────────────
def render_area_block(area: str, pages: list[Page]) -> str:
    members = [p for p in pages if area in p.areas]
    by_type: dict[str, list[Page]] = {}
    for p in members:
        by_type.setdefault(p.type or "", []).append(p)

    blocks: list[str] = []
    for ptype, title, folder in _TYPE_SECTIONS:
        sel = by_type.get(ptype, [])
        if not sel and ptype in ("comparison",):
            continue
        blocks += [
            f"## {title}",
            "",
            "```dataview",
            f"TABLE tags FROM \"wiki/{folder}\" "
            f"WHERE contains(areas, \"{area}\") SORT file.name ASC",
            "```",
            "",
            _list_links(sel),
            "",
        ]
    return "\n".join(blocks).rstrip()


def update_area_file(path: Path, area: str, pages: list[Page]) -> bool:
    """Reescribe el bloque auto de un MOC existente. Devuelve True si cambió.

    Si el archivo ya tiene marcadores, reemplaza entre ellos. Si no (migración
    desde el formato manual), reemplaza desde el primer encabezado ``## `` hasta
    el final, preservando frontmatter, título H1 y la descripción humana.
    """
    text = path.read_text(encoding="utf-8")
    block = render_area_block(area, pages)
    if _AUTO_START in text:
        new = _replace_auto_block(text, block)
    else:
        m = re.search(r"^## ", text, flags=re.MULTILINE)
        preamble = text[:m.start()].rstrip() if m else text.rstrip()
        new = f"{preamble}\n\n{_AUTO_START}\n{block}\n{_AUTO_END}\n"
    new = _bump_updated(new)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def generate(wiki_dir: Path) -> list[str]:
    """Regenera index.md y todos los MOCs. Devuelve rutas modificadas."""
    pages = load_wiki(wiki_dir)
    changed: list[str] = []

    index_path = wiki_dir / "index.md"
    new_index = render_index(pages)
    old_index = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    if new_index != old_index:
        index_path.write_text(new_index, encoding="utf-8")
        changed.append(index_path.relative_to(wiki_dir.parent).as_posix())

    for area in _AREAS:
        ap = wiki_dir / "areas" / f"{area}.md"
        if ap.exists() and update_area_file(ap, area, pages):
            changed.append(ap.relative_to(wiki_dir.parent).as_posix())

    return changed
