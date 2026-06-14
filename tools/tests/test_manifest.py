from __future__ import annotations

from pathlib import Path

from atlas_local.manifest import Manifest, Status


def _pdf(raw: Path, name: str, content: bytes = b"%PDF-1.4 hello") -> Path:
    p = raw / name
    p.write_bytes(content)
    return p


def test_pending_when_unknown(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    pdf = _pdf(raw, "a.pdf")
    m = Manifest.load(raw)
    assert m.status_of(pdf) is Status.PENDING


def test_converted_after_record(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    pdf = _pdf(raw, "a.pdf")
    md = pdf.with_suffix(".md")
    md.write_text("# md", encoding="utf-8")
    m = Manifest.load(raw)
    m.record(pdf, md_path=md, extractor="marker", extractor_version="1", device="cpu")
    assert m.status_of(pdf) is Status.CONVERTED


def test_stale_when_pdf_changes(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    pdf = _pdf(raw, "a.pdf")
    md = pdf.with_suffix(".md")
    md.write_text("# md", encoding="utf-8")
    m = Manifest.load(raw)
    m.record(pdf, md_path=md, extractor="marker", extractor_version="1", device="cpu")
    pdf.write_bytes(b"%PDF-1.4 CHANGED")
    assert m.status_of(pdf) is Status.STALE


def test_pending_when_md_missing(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    pdf = _pdf(raw, "a.pdf")
    md = pdf.with_suffix(".md")
    md.write_text("# md", encoding="utf-8")
    m = Manifest.load(raw)
    m.record(pdf, md_path=md, extractor="marker", extractor_version="1", device="cpu")
    md.unlink()
    assert m.status_of(pdf) is Status.PENDING


def test_save_and_reload(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    pdf = _pdf(raw, "a.pdf")
    md = pdf.with_suffix(".md")
    md.write_text("# md", encoding="utf-8")
    m = Manifest.load(raw)
    m.record(pdf, md_path=md, extractor="marker", extractor_version="1", device="cpu")
    m.save()
    again = Manifest.load(raw)
    assert again.status_of(pdf) is Status.CONVERTED
