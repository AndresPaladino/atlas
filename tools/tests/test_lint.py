from __future__ import annotations

from atlas_local.wiki.lint import lint
from tests.conftest import write_page


def _checks(findings):
    return {f.check for f in findings}


def test_clean_wiki_has_no_graph_errors(wiki):
    findings = lint(wiki)
    # gradient ⇄ greens son consistentes; sin links/aristas rotos.
    assert "broken-link" not in _checks(findings)
    assert "broken-edge" not in _checks(findings)
    assert "edge-asymmetric" not in _checks(findings)


def test_broken_link_detected(wiki):
    write_page(wiki, "concepts", "lonely",
               "type: concept\ntitle: Lonely\nareas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01",
               body="apunto a [[no-existe]].")
    findings = lint(wiki)
    assert any(f.check == "broken-link" and "no-existe" in f.message for f in findings)


def test_broken_edge_detected(wiki):
    write_page(wiki, "concepts", "dangling",
               "type: concept\ntitle: D\nareas: [math]\nrequires: ['[[fantasma]]']\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert any(f.check == "broken-edge" for f in lint(wiki))


def test_edge_asymmetry_detected(wiki):
    # nuevo nodo que requiere gradient pero gradient no lo desbloquea
    write_page(wiki, "concepts", "asym",
               "type: concept\ntitle: A\nareas: [math]\nrequires: ['[[gradient]]']\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert any(f.check == "edge-asymmetric" for f in lint(wiki))


def test_assessment_symmetry_detected(wiki):
    # un examen evalúa gradient pero gradient no tiene assessed_by hacia él
    write_page(wiki, "assessments", "exam-x",
               "type: assessment\ntitle: E\nassessment_kind: exam\nareas: [math]\n"
               "path: raw/e.pdf\nevaluates: ['[[gradient]]']\n"
               "created: 2026-01-01\nupdated: 2026-01-01")
    assert any(f.check == "assessment-symmetry" for f in lint(wiki))


def test_orphan_detected(wiki):
    write_page(wiki, "concepts", "island",
               "type: concept\ntitle: Island\nareas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert any(f.check == "orphan" and "island" in f.location for f in lint(wiki))


def test_source_not_ingested(wiki, tmp_path):
    raw = wiki.parent / "raw"
    raw.mkdir()
    (raw / "paper.pdf").write_bytes(b"%PDF-1.4 fake")
    findings = lint(wiki, raw_dir=raw)
    assert any(f.check == "source-not-ingested" for f in findings)


def test_solution_path_counts_as_ingested(wiki):
    # el PDF de solución lo referencia la propia página del examen vía
    # solution_path:, no una página aparte — no debe reportarse como huérfano
    raw = wiki.parent / "raw"
    raw.mkdir()
    (raw / "e.pdf").write_bytes(b"%PDF-1.4 fake")
    (raw / "e-sol.pdf").write_bytes(b"%PDF-1.4 fake")
    write_page(wiki, "assessments", "exam-x",
               "type: assessment\ntitle: E\nassessment_kind: exam\nareas: [math]\n"
               "path: raw/e.pdf\nsolution_path: raw/e-sol.pdf\n"
               "created: 2026-01-01\nupdated: 2026-01-01")
    findings = lint(wiki, raw_dir=raw)
    assert not [f for f in findings if f.check == "source-not-ingested"]
