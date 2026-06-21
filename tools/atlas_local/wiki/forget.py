"""``atlas forget``: eliminar una fuente del wiki sin romper entidades compartidas.

Al olvidar una fuente, cada página que la citaba en ``sources:`` pierde **solo
ese** wikilink. Una página sobrevive si le queda al menos otra fuente
(*shared-entity preservation*); se borra únicamente si quedaba sostenida por esa
sola fuente. La página de la fuente en ``wiki/sources/`` también se elimina.

El cálculo (``plan_forget``) es puro y testeable; la escritura (``apply_forget``)
está aislada para que el CLI confirme antes de tocar el filesystem.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .loader import Page, normalize_slug

# Línea inline de frontmatter: ``sources: ["[[a]]", "[[sources/b]]"]``.
_SOURCES_LINE = re.compile(r"^sources:[^\n]*\n", re.MULTILINE)
_WIKILINK_RAW = re.compile(r"\[\[[^\]]+\]\]")


@dataclass
class ForgetPlan:
    """Qué haría un ``forget`` — sin tocar nada todavía."""

    source_slug: str
    source_page: str | None = None          # rel_path de wiki/sources/<slug>.md, si existe
    unlinked: list[str] = field(default_factory=list)  # rel_paths que pierden la fuente (siguen vivas)
    deleted: list[str] = field(default_factory=list)   # rel_paths que quedan sin fuentes → se borran

    @property
    def is_empty(self) -> bool:
        return not (self.source_page or self.unlinked or self.deleted)

    def as_dict(self) -> dict:
        return {
            "source_slug": self.source_slug,
            "source_page": self.source_page,
            "unlinked": self.unlinked,
            "deleted": self.deleted,
        }


# ponytail: forget cubre sources (arista `sources:`), no assessments (arista
# `assessed_by:`). Olvidar un examen no fue pedido; agregar una rama análoga
# cuando haga falta — el patrón es idéntico cambiando folder/arista.
def plan_forget(pages: list[Page], source_slug: str) -> ForgetPlan:
    """Computa el plan de olvido de ``source_slug`` sobre las páginas dadas."""
    slug = normalize_slug(source_slug)
    plan = ForgetPlan(source_slug=slug)
    for p in pages:
        if p.folder == "sources" and p.slug == slug:
            plan.source_page = p.rel_path
            continue
        srcs = p.edge("sources")
        if slug not in srcs:
            continue
        if any(s != slug for s in srcs):
            plan.unlinked.append(p.rel_path)
        else:
            plan.deleted.append(p.rel_path)
    return plan


def _rewrite_sources(text: str, source_slug: str) -> str | None:
    """Quita el wikilink de ``source_slug`` de la línea inline ``sources:``.

    Preserva los wikilinks restantes tal cual están escritos (incluido un prefijo
    ``sources/`` si lo tienen). Devuelve None si no hay línea inline con
    wikilinks (p.ej. lista en formato bloque ``- ``), para no corromper el archivo.
    """
    m = _SOURCES_LINE.search(text)
    if not m:
        return None
    line = m.group(0)
    raw_links = _WIKILINK_RAW.findall(line)
    if not raw_links:
        return None
    kept = [l for l in raw_links if normalize_slug(l[2:-2]) != source_slug]
    items = ", ".join('"' + l + '"' for l in kept)
    new_line = f"sources: [{items}]\n"
    return text[: m.start()] + new_line + text[m.end():]


def apply_forget(repo_root: Path, plan: ForgetPlan) -> list[str]:
    """Ejecuta el plan. Devuelve los rel_paths efectivamente modificados/borrados."""
    touched: list[str] = []
    for rel in plan.unlinked:
        path = repo_root / rel
        text = path.read_text(encoding="utf-8")
        new = _rewrite_sources(text, plan.source_slug)
        if new is not None and new != text:
            path.write_text(new, encoding="utf-8")
            touched.append(rel)
    for rel in plan.deleted:
        (repo_root / rel).unlink(missing_ok=True)
        touched.append(rel)
    if plan.source_page:
        (repo_root / plan.source_page).unlink(missing_ok=True)
        touched.append(plan.source_page)
    return touched
