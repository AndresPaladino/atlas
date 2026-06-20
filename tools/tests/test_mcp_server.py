from __future__ import annotations

import pytest

pytest.importorskip("mcp")  # solo corre si el extra [mcp] está instalado

from atlas_local import mcp_server as srv


@pytest.fixture
def atlas_root(wiki, monkeypatch):
    """Apunta el servidor MCP al repo de fixture (wiki.parent)."""
    monkeypatch.setenv("ATLAS_ROOT", str(wiki.parent))
    return wiki.parent


def test_query_index_summary(atlas_root):
    out = srv.atlas_query_index()
    assert out["count"] == 2
    assert out["blocked_count"] == 0
    assert "areas" in out and "tags" in out and "types" in out
    # no debe incluir lista de páginas (evita volcar ~18k tokens)
    assert "pages" not in out


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
    # el índice reporta páginas bloqueadas en el conteo
    idx = srv.atlas_query_index()
    assert idx["blocked_count"] >= 1


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
