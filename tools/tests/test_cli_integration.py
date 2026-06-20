"""Tests de integración: invocan el app Typer de punta a punta.

Complementan los unit tests de lógica pura comprobando que el CLI
(parsing de args, _require_wiki, salida, exit codes) funciona correctamente.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from atlas_local.cli import app
from tests.conftest import write_page

runner = CliRunner()


# ── validate ────────────────────────────────────────────────────────────────


def test_validate_clean_wiki_exits_zero(wiki):
    result = runner.invoke(app, ["validate", "--wiki", str(wiki)])
    assert result.exit_code == 0
    assert "0 errores" in result.output


def test_validate_bad_page_exits_nonzero(wiki):
    write_page(wiki, "concepts", "broken",
               # type falta → error de schema
               "title: Broken\nareas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    result = runner.invoke(app, ["validate", "--wiki", str(wiki)])
    assert result.exit_code != 0
    assert "error" in result.output.lower()


def test_validate_missing_wiki_exits_nonzero(tmp_path):
    result = runner.invoke(app, ["validate", "--wiki", str(tmp_path / "nowhere")])
    assert result.exit_code != 0


# ── lint ────────────────────────────────────────────────────────────────────


def test_lint_clean_wiki_exits_zero(wiki):
    result = runner.invoke(app, ["lint", "--wiki", str(wiki)])
    assert result.exit_code == 0
    assert "Sin findings" in result.output


def test_lint_broken_link_reported(wiki):
    write_page(wiki, "concepts", "broken",
               "type: concept\ntitle: B\nareas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01",
               body="ver [[no-existe]].")
    result = runner.invoke(app, ["lint", "--wiki", str(wiki)])
    assert "broken-link" in result.output


def test_lint_json_output_is_valid(wiki):
    import json
    result = runner.invoke(app, ["lint", "--wiki", str(wiki), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "findings" in data


# ── index ────────────────────────────────────────────────────────────────────


def test_index_creates_index_file(wiki):
    result = runner.invoke(app, ["index", "--wiki", str(wiki)])
    assert result.exit_code == 0
    index = wiki / "index.md"
    assert index.exists()
    content = index.read_text()
    assert "gradient" in content
    assert "greens-theorem" in content
