from __future__ import annotations

from pathlib import Path

from atlas_local.wiki.ingest import ingest_status, source_status, stamp_source
from atlas_local.wiki.loader import load_wiki

from .conftest import write_page


def _source_with_raw(wiki: Path, slug: str, raw_text: str) -> None:
    repo_root = wiki.parent
    raw_dir = repo_root / "raw"
    raw_dir.mkdir(exist_ok=True)
    (raw_dir / f"{slug}.md").write_text(raw_text, encoding="utf-8")
    write_page(wiki, "sources", slug,
               f"type: source\ntitle: {slug}\nsource_kind: notes\n"
               f"path: raw/{slug}.pdf\nextracted: raw/{slug}.md\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")


def _source_page(wiki: Path, slug: str):
    return next(p for p in load_wiki(wiki) if p.folder == "sources" and p.slug == slug)


def test_new_source_has_no_hash(wiki):
    _source_with_raw(wiki, "book", "contenido original")
    st = source_status(wiki.parent, _source_page(wiki, "book"))
    assert st.status == "new"


def test_stamp_then_current(wiki):
    _source_with_raw(wiki, "book", "contenido original")
    digest = stamp_source(wiki.parent, _source_page(wiki, "book"))
    assert digest
    # tras sellar, el estado es current (reload para tomar el frontmatter nuevo)
    st = source_status(wiki.parent, _source_page(wiki, "book"))
    assert st.status == "current"


def test_changed_raw_is_stale(wiki):
    _source_with_raw(wiki, "book", "contenido original")
    stamp_source(wiki.parent, _source_page(wiki, "book"))
    # el raw cambia → stale
    (wiki.parent / "raw" / "book.md").write_text("contenido EDITADO", encoding="utf-8")
    st = source_status(wiki.parent, _source_page(wiki, "book"))
    assert st.status == "stale"


def test_missing_raw(wiki):
    write_page(wiki, "sources", "ghost",
               "type: source\ntitle: ghost\nsource_kind: notes\npath: raw/ghost.pdf\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    st = source_status(wiki.parent, _source_page(wiki, "ghost"))
    assert st.status == "missing-raw"


def test_ingest_status_only_sources(wiki):
    _source_with_raw(wiki, "book", "x")
    statuses = ingest_status(load_wiki(wiki), wiki.parent)
    assert [s.slug for s in statuses] == ["book"]


def test_stamp_is_idempotent(wiki):
    _source_with_raw(wiki, "book", "x")
    d1 = stamp_source(wiki.parent, _source_page(wiki, "book"))
    d2 = stamp_source(wiki.parent, _source_page(wiki, "book"))
    assert d1 == d2
    # no se duplica la línea en el frontmatter
    text = (wiki / "sources" / "book.md").read_text(encoding="utf-8")
    assert text.count("ingested_sha256:") == 1
