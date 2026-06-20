from __future__ import annotations

from pathlib import Path

from atlas_local.wiki.forget import apply_forget, plan_forget
from atlas_local.wiki.loader import load_wiki

from .conftest import write_page


def _wiki_with_two_sources(wiki: Path) -> None:
    """eigenvalue citado por DOS fuentes; determinant por UNA sola."""
    write_page(wiki, "sources", "exam-a",
               "type: source\ntitle: Examen A\nsource_kind: notes\npath: raw/exam-a.pdf\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    write_page(wiki, "sources", "notes-b",
               "type: source\ntitle: Notas B\nsource_kind: notes\npath: raw/notes-b.pdf\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    write_page(wiki, "concepts", "eigenvalue",
               "type: concept\ntitle: Autovalor\nareas: [math]\n"
               "sources: ['[[exam-a]]', '[[notes-b]]']\ncreated: 2026-01-01\nupdated: 2026-01-01")
    write_page(wiki, "concepts", "determinant",
               "type: concept\ntitle: Determinante\nareas: [math]\n"
               "sources: ['[[exam-a]]']\ncreated: 2026-01-01\nupdated: 2026-01-01")


def test_plan_preserves_shared_entity(wiki):
    _wiki_with_two_sources(wiki)
    plan = plan_forget(load_wiki(wiki), "exam-a")
    assert plan.source_page == "wiki/sources/exam-a.md"
    # eigenvalue tiene otra fuente → solo pierde el link
    assert "wiki/concepts/eigenvalue.md" in plan.unlinked
    # determinant quedaba solo con exam-a → se borra
    assert "wiki/concepts/determinant.md" in plan.deleted


def test_apply_forget_rewrites_and_deletes(wiki):
    _wiki_with_two_sources(wiki)
    repo_root = wiki.parent
    plan = plan_forget(load_wiki(wiki), "exam-a")
    apply_forget(repo_root, plan)

    # eigenvalue sigue existiendo, sin exam-a pero con notes-b
    eig = (wiki / "concepts" / "eigenvalue.md").read_text(encoding="utf-8")
    assert "exam-a" not in eig
    assert "[[notes-b]]" in eig
    # determinant y la página de fuente fueron borradas
    assert not (wiki / "concepts" / "determinant.md").exists()
    assert not (wiki / "sources" / "exam-a.md").exists()


def test_forget_handles_sources_folder_prefix(wiki):
    """Tolera el formato [[sources/slug]] (migración de prefijo de carpeta)."""
    write_page(wiki, "sources", "exam-a",
               "type: source\ntitle: Examen A\nsource_kind: notes\npath: raw/exam-a.pdf\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    write_page(wiki, "concepts", "eigenvalue",
               "type: concept\ntitle: Autovalor\nareas: [math]\n"
               "sources: ['[[sources/exam-a]]', '[[sources/notes-b]]']\n"
               "created: 2026-01-01\nupdated: 2026-01-01")
    plan = plan_forget(load_wiki(wiki), "exam-a")
    assert "wiki/concepts/eigenvalue.md" in plan.unlinked
    apply_forget(wiki.parent, plan)
    eig = (wiki / "concepts" / "eigenvalue.md").read_text(encoding="utf-8")
    assert "exam-a" not in eig
    assert "[[sources/notes-b]]" in eig


def test_forget_handles_alias_in_wikilink(wiki):
    """Tolera [[slug|alias]] en la línea de sources: del frontmatter."""
    write_page(wiki, "sources", "exam-a",
               "type: source\ntitle: Examen A\nsource_kind: notes\npath: raw/exam-a.pdf\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    write_page(wiki, "sources", "notes-b",
               "type: source\ntitle: Notas B\nsource_kind: notes\npath: raw/notes-b.pdf\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    write_page(wiki, "concepts", "eigenvalue",
               "type: concept\ntitle: Autovalor\nareas: [math]\n"
               "sources: ['[[exam-a|Examen A]]', '[[notes-b|Notas B]]']\n"
               "created: 2026-01-01\nupdated: 2026-01-01")
    plan = plan_forget(load_wiki(wiki), "exam-a")
    assert "wiki/concepts/eigenvalue.md" in plan.unlinked
    apply_forget(wiki.parent, plan)
    eig = (wiki / "concepts" / "eigenvalue.md").read_text(encoding="utf-8")
    assert "exam-a" not in eig
    assert "[[notes-b|Notas B]]" in eig


def test_forget_unknown_source_is_empty(wiki):
    plan = plan_forget(load_wiki(wiki), "no-existe")
    assert plan.is_empty
