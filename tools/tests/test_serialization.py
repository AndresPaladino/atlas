"""Contrato dict→JSON que consumirá el MCP, y guardas de regresión de Fase 0."""

from __future__ import annotations

import json

from atlas_local.wiki.forget import ForgetPlan
from atlas_local.wiki.index import render_area_block, render_index
from atlas_local.wiki.ingest import SourceStatus
from atlas_local.wiki.loader import load_wiki


def test_dataclasses_are_json_serializable():
    plan = ForgetPlan(source_slug="x", source_page="wiki/sources/x.md",
                      unlinked=["wiki/concepts/a.md"], deleted=["wiki/concepts/b.md"])
    st = SourceStatus(slug="x", status="current", raw_path="raw/x.md")
    # No deben lanzar: el MCP serializa estos dicts tal cual.
    json.dumps(plan.as_dict())
    json.dumps(st.as_dict())


def test_index_has_no_dataview_only_plaintext(wiki):
    pages = load_wiki(wiki)
    rendered = render_index(pages)
    assert "dataview" not in rendered
    assert "- [[" in rendered  # lista plana presente


def test_area_moc_has_no_dataview(wiki):
    pages = load_wiki(wiki)
    block = render_area_block("math", pages)
    assert "dataview" not in block
