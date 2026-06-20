"""Servidor MCP de Atlas — expone el grafo del wiki como tools MCP.

Envuelve las funciones puras de ``atlas_local.wiki.*`` (loader, schema, lint,
session, ingest) como tools. Sin Rich, sin prints: I/O por JSON. El firewall de
``/practice`` se enforça acá —``atlas_read_page`` consulta ``session.check_read``—
así que ningún cliente MCP puede saltarlo, igual que el hook de Claude Code.

Correr: ``atlas-mcp`` (transporte stdio). Requiere ``ATLAS_ROOT`` apuntando al
repo, o ejecutarse dentro de él. Instalar con el extra: ``atlas[mcp]``.
"""

from __future__ import annotations

import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .wiki import ingest as ingest_mod
from .wiki import lint as lint_mod
from .wiki import session as session_mod
from .wiki.loader import Page, load_wiki
from .wiki.paths import find_repo_root
from .wiki.schema import validate_page

logger = logging.getLogger("atlas_mcp")

mcp = FastMCP("atlas")


def _repo_root() -> Path:
    root = find_repo_root()
    if root is None:
        raise RuntimeError(
            "No encuentro el repo Atlas. Seteá ATLAS_ROOT o corré atlas-mcp dentro del repo."
        )
    return root


def _page_summary(p: Page) -> dict:
    return {
        "slug": p.slug,
        "type": p.type,
        "title": p.frontmatter.get("title"),
        "areas": p.areas,
        "tags": p.tags,
        "folder": p.folder,
    }


# ── consulta del grafo ──────────────────────────────────────────────────────────
@mcp.tool()
def atlas_query_index() -> dict:
    """Resumen del wiki: conteo, áreas, tipos y tags disponibles.

    Devuelve metadatos agregados, NO la lista de páginas (evita volcar ~18k tokens).
    Para encontrar páginas específicas usá atlas_search(query).
    Para leer una página usá atlas_read_page(slug).
    """
    root = _repo_root()
    pages = load_wiki(root / "wiki")
    sess = session_mod.load_session(root)
    blocked_count = 0
    if sess.mode == "practice" and not sess.reveal:
        blocked = set(sess.blocked_slugs)
        blocked_count = sum(1 for p in pages if p.slug in blocked)

    areas: set[str] = set()
    tags: set[str] = set()
    types: dict[str, int] = {}
    for p in pages:
        areas.update(p.areas)
        tags.update(p.tags)
        types[p.type] = types.get(p.type, 0) + 1

    return {
        "count": len(pages),
        "blocked_count": blocked_count,
        "areas": sorted(areas),
        "tags": sorted(tags),
        "types": types,
        "hint": "Usá atlas_search(query) para encontrar páginas. atlas_read_page(slug) para leer el contenido.",
    }


@mcp.tool()
def atlas_read_page(slug: str) -> dict:
    """Lee una página del wiki por slug (frontmatter + cuerpo).

    Respeta el firewall de /practice: si la página está bloqueada devuelve
    `denied: true` sin contenido.
    """
    root = _repo_root()
    page = next((p for p in load_wiki(root / "wiki") if p.slug == slug), None)
    if page is None:
        return {"found": False, "slug": slug}
    allowed, reason = session_mod.check_read(root, page.path)
    if not allowed:
        return {"found": True, "slug": slug, "denied": True, "reason": reason}
    return {
        "found": True,
        "slug": slug,
        "denied": False,
        "rel_path": page.rel_path,
        "frontmatter": page.frontmatter,
        "body": page.body,
    }


@mcp.tool()
def atlas_search(query: str, limit: int = 20) -> dict:
    """Busca páginas por coincidencia (substring, case-insensitive) en slug,
    título, aliases o tags."""
    q = query.strip().lower()
    hits: list[dict] = []
    for p in load_wiki(_repo_root() / "wiki"):
        hay = [p.slug, str(p.frontmatter.get("title", ""))]
        hay += [str(a) for a in p.aliases]
        hay += [str(t) for t in p.tags]
        if any(q in h.lower() for h in hay):
            hits.append(_page_summary(p))
    return {"query": query, "count": len(hits), "results": hits[:limit]}


# ── auditoría ─────────────────────────────────────────────────────────────────
@mcp.tool()
def atlas_lint(scope: str | None = None) -> dict:
    """Audita la consistencia del wiki (orphans, links/aristas rotos, simetría, drift)."""
    root = _repo_root()
    raw = root / "raw"
    findings = lint_mod.lint(root / "wiki", scope=scope, raw_dir=raw if raw.is_dir() else None)
    return {"count": len(findings), "findings": [f.as_dict() for f in findings]}


@mcp.tool()
def atlas_validate() -> dict:
    """Valida el frontmatter de todas las páginas contra el contrato."""
    out: list[dict] = []
    for p in load_wiki(_repo_root() / "wiki"):
        errs = validate_page(p)
        if errs:
            out.append({"page": p.rel_path, "errors": errs})
    return {"pages_with_issues": len(out), "issues": out}


@mcp.tool()
def atlas_ingest_status() -> dict:
    """Estado de ingestión raw→wiki de cada fuente (new/stale/current/missing-raw)."""
    root = _repo_root()
    statuses = ingest_mod.ingest_status(load_wiki(root / "wiki"), root)
    return {"sources": [s.as_dict() for s in statuses]}


# ── sesión / firewall ───────────────────────────────────────────────────────────
@mcp.tool()
def atlas_session_set(topic: str) -> dict:
    """Arranca una sesión /practice sobre el tema T y calcula los slugs bloqueados."""
    root = _repo_root()
    return session_mod.set_practice(root, root / "wiki", topic).as_dict()


@mcp.tool()
def atlas_session_mode(mode: str) -> dict:
    """Cambia el modo (query|practice|ingest|lint). Cualquiera ≠ practice baja el firewall."""
    return session_mod.set_mode(_repo_root(), mode).as_dict()


@mcp.tool()
def atlas_session_reveal(value: bool = True) -> dict:
    """Válvula de escape del firewall: permite la próxima lectura bloqueada."""
    return session_mod.set_reveal(_repo_root(), value).as_dict()


@mcp.tool()
def atlas_session_clear() -> dict:
    """Resetea la sesión (modo query, sin bloqueos)."""
    return session_mod.clear(_repo_root()).as_dict()


@mcp.tool()
def atlas_session_show() -> dict:
    """Muestra el estado de sesión actual (modo, T, slugs bloqueados, reveal)."""
    return session_mod.load_session(_repo_root()).as_dict()


def main() -> None:
    """Entry point del servidor MCP (stdio)."""
    logging.basicConfig(level=logging.INFO)
    mcp.run()


if __name__ == "__main__":
    main()
