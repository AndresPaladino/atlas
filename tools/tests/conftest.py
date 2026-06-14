"""Fixtures compartidos: construcción de wikis mínimos en tmp_path."""

from __future__ import annotations

from pathlib import Path

import pytest


def write_page(wiki: Path, folder: str, slug: str, frontmatter: str, body: str = "cuerpo.") -> Path:
    d = wiki / folder
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{slug}.md"
    p.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body}\n", encoding="utf-8")
    return p


@pytest.fixture
def wiki(tmp_path: Path) -> Path:
    """Un wiki mínimo y consistente con dos conceptos y un teorema."""
    root = tmp_path / "repo"
    (root / "schema").mkdir(parents=True)
    w = root / "wiki"
    w.mkdir()
    write_page(
        w, "concepts", "gradient",
        "type: concept\ntitle: Gradiente\nareas: [math]\n"
        "unlocks: ['[[greens-theorem]]']\ncreated: 2026-01-01\nupdated: 2026-01-01",
        body="El gradiente. Ver [[greens-theorem]].",
    )
    write_page(
        w, "theorems", "greens-theorem",
        "type: theorem\ntitle: Teorema de Green\naliases: [Green]\nareas: [math]\n"
        "statement_form: 'if C then D'\nrequires: ['[[gradient]]']\n"
        "created: 2026-01-01\nupdated: 2026-01-01",
    )
    return w
