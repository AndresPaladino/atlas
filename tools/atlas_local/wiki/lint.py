"""Checks de consistencia del wiki, en código.

Reemplaza la detección que ``schema/lint-protocol.md`` hacía pedirle a un LLM
sobre 56 archivos. Acá los checks determinísticos (grafo, frontmatter, fechas)
son funciones puras y reproducibles. El modo ``/lint`` consume ``--json`` y se
limita a discutir y aplicar los fixes — el juicio, no la detección.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from .loader import Page, index_by_slug, load_wiki
from .schema import validate_page

# Aristas de frontmatter que cuentan como "referencia entrante" a otra página.
_EDGE_KEYS = (
    "requires", "unlocks", "sources", "illustrates", "compares",
    "covers_concepts", "covers_theorems", "covers_methods",
    "evaluates", "assessed_by",
)

# Tipos que son raíces del grafo: nunca son orphans.
_ROOT_TYPES = frozenset({"area", "source", "assessment"})


@dataclass
class Finding:
    check: str          # "orphan", "broken-link", ...
    severity: str       # "error" | "warning"
    location: str       # archivo[:línea] o slug
    message: str

    def as_dict(self) -> dict:
        return asdict(self)


def _resolvable(pages: list[Page]) -> set[str]:
    """Conjunto de identificadores que un wikilink puede resolver: slugs + aliases."""
    ids: set[str] = set()
    for p in pages:
        ids.add(p.slug)
        for a in p.aliases:
            ids.add(str(a).strip())
    return ids


def _inbound_targets(pages: list[Page]) -> Counter:
    """Cuenta cuántas veces cada slug es referenciado (cuerpo + aristas).

    Los MOCs (`type: area`) se excluyen: se generan y listan *todas* las páginas,
    así que contar sus links volvería inútil el check de orphans (nada sería
    orphan). El índice/log tampoco se cargan como páginas.
    """
    counter: Counter = Counter()
    for p in pages:
        if p.type == "area":
            continue
        for link in p.links:
            counter[link.target] += 1
        for key in _EDGE_KEYS:
            for tgt in p.edge(key):
                counter[tgt] += 1
    return counter


def lint(wiki_dir: Path, scope: str | None = None,
         raw_dir: Path | None = None) -> list[Finding]:
    """Corre todos los checks y devuelve los findings ordenados por severidad."""
    repo_root = wiki_dir.parent
    pages = load_wiki(wiki_dir, scope)
    by_slug = index_by_slug(pages)
    resolvable = _resolvable(pages)
    inbound = _inbound_targets(pages)
    findings: list[Finding] = []

    # ── 9. frontmatter / schema (delegado a schema.validate_page) ─────────────
    for p in pages:
        for err in validate_page(p):
            sev = "warning" if err.startswith("warn:") else "error"
            findings.append(Finding(
                "frontmatter-incomplete", sev, p.rel_path,
                err.removeprefix("warn: "),
            ))

    # ── 1. orphans ────────────────────────────────────────────────────────────
    for p in pages:
        if p.type in _ROOT_TYPES:
            continue
        if inbound.get(p.slug, 0) == 0 and not any(
            inbound.get(str(a).strip(), 0) for a in p.aliases
        ):
            findings.append(Finding(
                "orphan", "warning", p.rel_path,
                "sin wikilinks entrantes ni aristas que la referencien",
            ))

    # ── 2. broken-link (cuerpo) ───────────────────────────────────────────────
    for p in pages:
        for link in p.links:
            if link.target not in resolvable:
                findings.append(Finding(
                    "broken-link", "error", f"{p.rel_path}:{link.line}",
                    f"[[{link.target}]] no resuelve a ninguna página",
                ))

    # ── 3. broken-edge (requires/unlocks/sources/...) ─────────────────────────
    for p in pages:
        for key in _EDGE_KEYS:
            for tgt in p.edge(key):
                if tgt not in resolvable:
                    findings.append(Finding(
                        "broken-edge", "error", p.rel_path,
                        f"{key} → [[{tgt}]] no existe",
                    ))

    # ── 4. edge-asymmetric (requires ⇄ unlocks) ───────────────────────────────
    for p in pages:
        for tgt in p.edge("requires"):
            other = by_slug.get(tgt)
            if other is not None and p.slug not in other.edge("unlocks"):
                findings.append(Finding(
                    "edge-asymmetric", "warning", p.rel_path,
                    f"[[{p.slug}]] requires [[{tgt}]] pero [[{tgt}]] "
                    f"no tiene [[{p.slug}]] en unlocks",
                ))

    # ── 4b. assessment-symmetry (evaluates ⇄ assessed_by) ─────────────────────
    for p in pages:
        for tgt in p.edge("evaluates"):
            other = by_slug.get(tgt)
            if other is not None and p.slug not in other.edge("assessed_by"):
                findings.append(Finding(
                    "assessment-symmetry", "warning", p.rel_path,
                    f"[[{p.slug}]] evaluates [[{tgt}]] pero [[{tgt}]] "
                    f"no tiene [[{p.slug}]] en assessed_by",
                ))
        for tgt in p.edge("assessed_by"):
            other = by_slug.get(tgt)
            if other is not None and p.slug not in other.edge("evaluates"):
                findings.append(Finding(
                    "assessment-symmetry", "warning", p.rel_path,
                    f"[[{p.slug}]] assessed_by [[{tgt}]] pero [[{tgt}]] "
                    f"no tiene [[{p.slug}]] en evaluates",
                ))

    # ── 6 & 7 ya cubiertos por schema (statement_form, when_to_use/fails_when) ─

    # ── 8. concept-implicit (≥3 menciones sin página) ─────────────────────────
    for target, count in inbound.items():
        if count >= 3 and target not in resolvable:
            findings.append(Finding(
                "concept-implicit", "warning", target,
                f"mencionado {count} veces como [[{target}]] pero sin página propia",
            ))

    # ── chunks-migration: extracted: apuntando a un chunk → migrar a chunks: ────
    for p in pages:
        if p.type != "source":
            continue
        extracted = str(p.frontmatter.get("extracted", "")).strip()
        if not extracted:
            continue
        # Un chunk vive en raw/<nombre>/<archivo>.md (3 partes: raw / dir / file)
        parts = Path(extracted).parts
        if len(parts) >= 3 and parts[0] == "raw":
            findings.append(Finding(
                "chunks-migration", "warning", p.rel_path,
                f"extracted: apunta a un chunk ({extracted}); "
                f"migrá a chunks: [\"{extracted}\"] para tracking correcto",
            ))

    # ── 5. source-not-ingested (PDFs de raw/ sin página source) ───────────────
    if raw_dir and raw_dir.is_dir():
        ingested = {
            str(p.frontmatter.get("path", "")).strip()
            for p in pages if p.type in ("source", "assessment")
        }
        for pdf in sorted(raw_dir.rglob("*.pdf")):
            rel = pdf.relative_to(repo_root).as_posix()
            if rel not in ingested:
                findings.append(Finding(
                    "source-not-ingested", "warning", rel,
                    "PDF en raw/ sin página en wiki/sources|assessments/ que lo referencie",
                ))

    order = {"error": 0, "warning": 1}
    findings.sort(key=lambda f: (order[f.severity], f.check, f.location))
    return findings
