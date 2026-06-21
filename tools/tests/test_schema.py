from __future__ import annotations

from atlas_local.wiki.loader import load_page
from atlas_local.wiki.schema import validate_page
from tests.conftest import write_page


def _page(wiki, folder, slug, fm):
    p = write_page(wiki, folder, slug, fm)
    return load_page(p, wiki.parent)


def test_valid_pages_have_no_errors(wiki):
    for p in load_page_all(wiki):
        errs = [e for e in validate_page(p) if not e.startswith("warn:")]
        assert errs == [], (p.slug, errs)


def load_page_all(wiki):
    from atlas_local.wiki.loader import load_wiki
    return load_wiki(wiki)


def test_missing_required_field(wiki):
    p = _page(wiki, "concepts", "x", "type: concept\ntitle: X\ncreated: 2026-01-01\nupdated: 2026-01-01")
    errs = validate_page(p)
    assert any("areas" in e for e in errs)


def test_theorem_requires_statement_form(wiki):
    p = _page(wiki, "theorems", "t", "type: theorem\ntitle: T\nareas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert any("statement_form" in e for e in validate_page(p))


def test_method_requires_applicability(wiki):
    p = _page(wiki, "methods", "m", "type: method\ntitle: M\nareas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    errs = validate_page(p)
    assert any("when_to_use" in e for e in errs) and any("fails_when" in e for e in errs)


def test_unknown_area_is_warning(wiki):
    p = _page(wiki, "concepts", "z", "type: concept\ntitle: Z\nareas: [unobtanium]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert any(e.startswith("warn:") and "unobtanium" in e for e in validate_page(p))


def test_bad_type(wiki):
    p = _page(wiki, "concepts", "w", "type: gizmo\ntitle: W\nareas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert any("type" in e for e in validate_page(p))


def test_assessment_valid(wiki):
    p = _page(wiki, "assessments", "exam1",
              "type: assessment\ntitle: E\nassessment_kind: exam\nareas: [math]\n"
              "path: raw/e.pdf\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert [e for e in validate_page(p) if not e.startswith("warn:")] == []


def test_assessment_requires_kind_and_path(wiki):
    p = _page(wiki, "assessments", "exam2",
              "type: assessment\ntitle: E\nareas: [math]\ncreated: 2026-01-01\nupdated: 2026-01-01")
    errs = validate_page(p)
    assert any("assessment_kind" in e for e in errs) and any("path" in e for e in errs)


def test_assessment_bad_kind(wiki):
    p = _page(wiki, "assessments", "exam3",
              "type: assessment\ntitle: E\nassessment_kind: quiz\nareas: [math]\n"
              "path: raw/e.pdf\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert any("assessment_kind inválido" in e for e in validate_page(p))


def test_wrong_folder(wiki):
    # un theorem viviendo en concepts/
    p = _page(wiki, "concepts", "mis", "type: theorem\ntitle: Mis\nareas: [math]\nstatement_form: 'if a then b'\ncreated: 2026-01-01\nupdated: 2026-01-01")
    assert any("debería vivir" in e for e in validate_page(p))
