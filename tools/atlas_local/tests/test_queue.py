"""Tests para wiki/queue.py — cola de ingest persistente."""

import pytest
from pathlib import Path

from atlas_local.wiki.queue import (
    Queue, QueueItem,
    add_item, clear_done, done_item, fail_item, load_queue,
    save_queue, start_item, update_item,
)


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return tmp_path


def test_load_empty(root):
    q = load_queue(root)
    assert q.items == []
    assert q.version == 1


def test_add_item(root):
    item = add_item(root, "DDSE.pdf", chunks_total=178)
    assert item.status == "pending"
    assert item.chunks_total == 178
    assert item.pdf_key == "DDSE.pdf"

    q = load_queue(root)
    assert len(q.items) == 1


def test_add_item_idempotent(root):
    add_item(root, "DDSE.pdf", chunks_total=178)
    add_item(root, "DDSE.pdf", chunks_total=178)
    assert len(load_queue(root).items) == 1


def test_start_item(root):
    add_item(root, "DDSE.pdf")
    item = start_item(root, "DDSE.pdf")
    assert item.status == "in-progress"
    assert item.started_at is not None


def test_start_item_missing(root):
    assert start_item(root, "missing.pdf") is None


def test_update_item(root):
    add_item(root, "DDSE.pdf", chunks_total=3)
    start_item(root, "DDSE.pdf")
    update_item(root, "DDSE.pdf", "00-intro.md", source_slug="ddse-ch1")
    update_item(root, "DDSE.pdf", "01-svd.md")

    item = load_queue(root).get("DDSE.pdf")
    assert len(item.chunks_done) == 2
    assert item.source_slug == "ddse-ch1"
    assert item.progress == "2/3"


def test_update_item_no_duplicate_chunk(root):
    add_item(root, "DDSE.pdf", chunks_total=3)
    update_item(root, "DDSE.pdf", "00-intro.md")
    update_item(root, "DDSE.pdf", "00-intro.md")
    assert len(load_queue(root).get("DDSE.pdf").chunks_done) == 1


def test_done_item(root):
    add_item(root, "DDSE.pdf")
    done_item(root, "DDSE.pdf")
    assert load_queue(root).get("DDSE.pdf").status == "done"


def test_fail_item(root):
    add_item(root, "DDSE.pdf")
    fail_item(root, "DDSE.pdf")
    assert load_queue(root).get("DDSE.pdf").status == "failed"


def test_clear_done(root):
    add_item(root, "A.pdf")
    add_item(root, "B.pdf")
    add_item(root, "C.pdf")
    done_item(root, "A.pdf")
    fail_item(root, "B.pdf")
    n = clear_done(root)
    assert n == 2
    q = load_queue(root)
    assert len(q.items) == 1
    assert q.items[0].pdf_key == "C.pdf"


def test_in_progress_and_pending_filters(root):
    add_item(root, "A.pdf")
    add_item(root, "B.pdf")
    start_item(root, "A.pdf")
    q = load_queue(root)
    assert len(q.in_progress()) == 1
    assert len(q.pending()) == 1


def test_progress_no_chunks(root):
    item = QueueItem(pdf_key="X.pdf", chunks_total=0)
    assert item.progress == "—"


def test_persistence_survives_reload(root):
    add_item(root, "OS.pdf", chunks_total=258)
    start_item(root, "OS.pdf")
    update_item(root, "OS.pdf", "00-intro.md", source_slug="os-concepts")
    # reload
    q = load_queue(root)
    item = q.get("OS.pdf")
    assert item.status == "in-progress"
    assert item.source_slug == "os-concepts"
    assert item.chunks_done == ["00-intro.md"]
