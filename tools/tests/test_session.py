from __future__ import annotations

from atlas_local.wiki.session import (
    check_read, compute_blocked, load_session, set_practice, set_reveal, set_mode,
)


def test_compute_blocked_includes_neighborhood(wiki):
    blocked = compute_blocked(wiki, "Green")
    # la página de Green y su prerrequisito (gradient, vía requires) deben estar.
    assert "greens-theorem" in blocked
    assert "gradient" in blocked


def test_firewall_denies_blocked_allows_other(wiki):
    root = wiki.parent
    set_practice(root, wiki, "Green")
    blocked_page = wiki / "theorems" / "greens-theorem.md"
    allowed, reason = check_read(root, blocked_page)
    assert not allowed and "greens-theorem" in reason

    # un archivo de schema (fuera de wiki bloqueado) se permite
    other = root / "schema"
    other.mkdir(exist_ok=True)
    f = other / "foo.md"
    f.write_text("x", encoding="utf-8")
    allowed2, _ = check_read(root, f)
    assert allowed2


def test_reveal_opens_firewall(wiki):
    root = wiki.parent
    set_practice(root, wiki, "Green")
    set_reveal(root, True)
    allowed, _ = check_read(root, wiki / "theorems" / "greens-theorem.md")
    assert allowed


def test_mode_switch_lifts_firewall(wiki):
    root = wiki.parent
    set_practice(root, wiki, "Green")
    set_mode(root, "query")
    s = load_session(root)
    assert s.mode == "query" and s.blocked_slugs == []
    allowed, _ = check_read(root, wiki / "theorems" / "greens-theorem.md")
    assert allowed


def test_raw_is_blocked_in_practice(wiki):
    root = wiki.parent
    (root / "raw").mkdir(exist_ok=True)
    pdf = root / "raw" / "x.pdf"
    pdf.write_bytes(b"%PDF")
    set_practice(root, wiki, "Green")
    allowed, reason = check_read(root, pdf)
    assert not allowed and "raw/" in reason
