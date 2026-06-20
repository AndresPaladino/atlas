from __future__ import annotations

import json
from pathlib import Path

import pytest

from atlas_local.manifest import Manifest
from atlas_local.wiki.ingest import ingest_status, raw_ingest_status, source_status, stamp_source
from atlas_local.wiki.loader import load_wiki

from .conftest import write_page


# ── helpers ───────────────────────────────────────────────────────────────────

def _make_raw_dir(repo_root: Path) -> Path:
    raw = repo_root / "raw"
    raw.mkdir(exist_ok=True)
    return raw


def _register_pdf(raw_dir: Path, pdf_name: str, chunks: list[str] | None = None) -> Path:
    """Crea un PDF ficticio y lo registra en el Manifest."""
    pdf = raw_dir / pdf_name
    pdf.write_bytes(b"%PDF fake")
    manifest = Manifest.load(raw_dir)

    chunks_dir = None
    n_chunks = 0
    if chunks is not None:
        folder = raw_dir / pdf_name.replace(".pdf", "")
        folder.mkdir(exist_ok=True)
        for c in chunks:
            (folder / c).write_text(f"# {c}", encoding="utf-8")
        chunks_dir = folder
        n_chunks = len(chunks)

    md = raw_dir / pdf_name.replace(".pdf", ".md")
    md.write_text("# mono", encoding="utf-8")

    manifest.record(
        pdf,
        md_path=md,
        extractor="test",
        extractor_version="0",
        device="ci",
        n_chunks=n_chunks,
        chunks_dir=chunks_dir,
    )
    manifest.save()
    return pdf


def _source_page(wiki: Path, slug: str):
    return next(p for p in load_wiki(wiki) if p.folder == "sources" and p.slug == slug)


# ── tests: vista de frescura (source_status / ingest_status) ─────────────────

def _source_with_raw(wiki: Path, slug: str, raw_text: str) -> None:
    repo_root = wiki.parent
    raw_dir = _make_raw_dir(repo_root)
    (raw_dir / f"{slug}.md").write_text(raw_text, encoding="utf-8")
    write_page(wiki, "sources", slug,
               f"type: source\ntitle: {slug}\nsource_kind: notes\n"
               f"path: raw/{slug}.pdf\nextracted: raw/{slug}.md\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")


def test_new_source_has_no_hash(wiki):
    _source_with_raw(wiki, "book", "contenido original")
    st = source_status(wiki.parent, _source_page(wiki, "book"))
    assert st.status == "new"


def test_stamp_then_current(wiki):
    _source_with_raw(wiki, "book", "contenido original")
    digest = stamp_source(wiki.parent, _source_page(wiki, "book"))
    assert digest
    st = source_status(wiki.parent, _source_page(wiki, "book"))
    assert st.status == "current"


def test_changed_raw_is_stale(wiki):
    _source_with_raw(wiki, "book", "contenido original")
    stamp_source(wiki.parent, _source_page(wiki, "book"))
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


def test_null_sha256_treated_as_new(wiki):
    """ingested_sha256: null en el frontmatter → status 'new', no crash."""
    repo_root = wiki.parent
    raw_dir = _make_raw_dir(repo_root)
    (raw_dir / "book.md").write_text("contenido", encoding="utf-8")
    write_page(wiki, "sources", "book",
               "type: source\ntitle: book\nsource_kind: notes\n"
               "path: raw/book.pdf\nextracted: raw/book.md\n"
               "ingested_sha256: null\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    st = source_status(wiki.parent, _source_page(wiki, "book"))
    assert st.status == "new"


def test_malformed_sha256_treated_as_new(wiki):
    """ingested_sha256 con valor corto (no 64 hex) → status 'new'."""
    repo_root = wiki.parent
    raw_dir = _make_raw_dir(repo_root)
    (raw_dir / "book.md").write_text("contenido", encoding="utf-8")
    write_page(wiki, "sources", "book",
               "type: source\ntitle: book\nsource_kind: notes\n"
               "path: raw/book.pdf\nextracted: raw/book.md\n"
               "ingested_sha256: abc123\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    st = source_status(wiki.parent, _source_page(wiki, "book"))
    assert st.status == "new"


def test_stamp_is_idempotent(wiki):
    _source_with_raw(wiki, "book", "x")
    d1 = stamp_source(wiki.parent, _source_page(wiki, "book"))
    d2 = stamp_source(wiki.parent, _source_page(wiki, "book"))
    assert d1 == d2
    text = (wiki / "sources" / "book.md").read_text(encoding="utf-8")
    assert text.count("ingested_sha256:") == 1


# ── tests: vista de inventario (raw_ingest_status) ───────────────────────────

def test_pending_pdf_no_sources(wiki):
    raw_dir = _make_raw_dir(wiki.parent)
    _register_pdf(raw_dir, "libro.pdf")
    statuses = raw_ingest_status(load_wiki(wiki), raw_dir, wiki.parent)
    assert len(statuses) == 1
    s = statuses[0]
    assert s.pdf_key == "libro.pdf"
    assert s.status == "pending"
    assert s.sources == []


def test_ingested_pdf_simple(wiki):
    raw_dir = _make_raw_dir(wiki.parent)
    _register_pdf(raw_dir, "libro.pdf")
    write_page(wiki, "sources", "libro-ch1",
               "type: source\ntitle: Libro Ch1\nsource_kind: book\n"
               "path: raw/libro.pdf\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    statuses = raw_ingest_status(load_wiki(wiki), raw_dir, wiki.parent)
    assert statuses[0].status == "ingested"
    assert "libro-ch1" in statuses[0].sources


def test_partial_pdf_with_chunks(wiki):
    raw_dir = _make_raw_dir(wiki.parent)
    chunks = ["01-intro.md", "02-svd.md", "03-pca.md"]
    _register_pdf(raw_dir, "libro.pdf", chunks=chunks)
    # solo cubrimos un chunk via campo chunks: en el frontmatter
    write_page(wiki, "sources", "libro-intro",
               "type: source\ntitle: Libro Intro\nsource_kind: book\n"
               "path: raw/libro.pdf\n"
               "chunks: [raw/libro/01-intro.md]\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    statuses = raw_ingest_status(load_wiki(wiki), raw_dir, wiki.parent)
    s = statuses[0]
    assert s.status == "partial"
    assert s.n_chunks == 3
    assert len(s.covered_chunks) == 1
    assert s.uncovered_chunks_count == 2


def test_ingested_pdf_all_chunks_covered(wiki):
    raw_dir = _make_raw_dir(wiki.parent)
    chunks = ["01-intro.md", "02-svd.md"]
    _register_pdf(raw_dir, "libro.pdf", chunks=chunks)
    write_page(wiki, "sources", "libro-intro",
               "type: source\ntitle: Intro\nsource_kind: book\n"
               "path: raw/libro.pdf\n"
               "chunks: [raw/libro/01-intro.md]\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    write_page(wiki, "sources", "libro-svd",
               "type: source\ntitle: SVD\nsource_kind: book\n"
               "path: raw/libro.pdf\n"
               "chunks: [raw/libro/02-svd.md]\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    statuses = raw_ingest_status(load_wiki(wiki), raw_dir, wiki.parent)
    s = statuses[0]
    assert s.status == "ingested"
    assert s.uncovered_chunks_count == 0


def test_legacy_extracted_field_counts_as_chunk_coverage(wiki):
    """Sources viejas con extracted: apuntando a un chunk individual se reconocen."""
    raw_dir = _make_raw_dir(wiki.parent)
    chunks = ["01-intro.md", "02-svd.md"]
    _register_pdf(raw_dir, "libro.pdf", chunks=chunks)
    write_page(wiki, "sources", "libro-intro",
               "type: source\ntitle: Intro\nsource_kind: book\n"
               "path: raw/libro.pdf\n"
               "extracted: raw/libro/01-intro.md\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    statuses = raw_ingest_status(load_wiki(wiki), raw_dir, wiki.parent)
    s = statuses[0]
    assert s.status == "partial"
    assert "01-intro.md" in s.covered_chunks


def test_ordering_pending_first(wiki):
    raw_dir = _make_raw_dir(wiki.parent)
    _register_pdf(raw_dir, "aaa.pdf")
    _register_pdf(raw_dir, "bbb.pdf")
    write_page(wiki, "sources", "bbb-s",
               "type: source\ntitle: BBB\nsource_kind: book\n"
               "path: raw/bbb.pdf\n"
               "areas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    statuses = raw_ingest_status(load_wiki(wiki), raw_dir, wiki.parent)
    assert statuses[0].pdf_key == "aaa.pdf"
    assert statuses[0].status == "pending"
