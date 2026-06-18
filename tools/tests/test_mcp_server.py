from __future__ import annotations

import pytest

pytest.importorskip("mcp")  # solo corre si el extra [mcp] está instalado

from atlas_local import mcp_server as srv


@pytest.fixture
def atlas_root(wiki, monkeypatch):
    """Apunta el servidor MCP al repo de fixture (wiki.parent)."""
    monkeypatch.setenv("ATLAS_ROOT", str(wiki.parent))
    return wiki.parent


def test_query_index_lists_pages(atlas_root):
    out = srv.atlas_query_index()
    slugs = {p["slug"] for p in out["pages"]}
    assert out["count"] == 2
    assert {"gradient", "greens-theorem"} <= slugs
    # sin sesión practice, nada bloqueado
    assert all(not p["blocked"] for p in out["pages"])


def test_read_page_returns_body(atlas_root):
    out = srv.atlas_read_page("gradient")
    assert out["found"] and not out["denied"]
    assert "gradiente" in out["body"].lower()


def test_read_missing_page(atlas_root):
    assert srv.atlas_read_page("no-existe") == {"found": False, "slug": "no-existe"}


def test_firewall_denies_blocked_page(atlas_root):
    srv.atlas_session_set("Green")  # bloquea greens-theorem + vecindario
    out = srv.atlas_read_page("greens-theorem")
    assert out["denied"] is True
    assert "greens-theorem" in out["reason"]
    # el índice lo marca bloqueado
    idx = {p["slug"]: p for p in srv.atlas_query_index()["pages"]}
    assert idx["greens-theorem"]["blocked"] is True


def test_session_clear_lifts_firewall(atlas_root):
    srv.atlas_session_set("Green")
    srv.atlas_session_clear()
    out = srv.atlas_read_page("greens-theorem")
    assert out["denied"] is False and "body" in out


def test_reveal_lifts_firewall_once(atlas_root):
    srv.atlas_session_set("Green")
    srv.atlas_session_reveal(True)
    out = srv.atlas_read_page("greens-theorem")
    assert out["denied"] is False


def test_lint_and_validate_shapes(atlas_root):
    lint = srv.atlas_lint()
    assert "count" in lint and isinstance(lint["findings"], list)
    val = srv.atlas_validate()
    assert "issues" in val and isinstance(val["issues"], list)


def test_search(atlas_root):
    out = srv.atlas_search("green")
    assert out["count"] >= 1
    assert any(r["slug"] == "greens-theorem" for r in out["results"])
