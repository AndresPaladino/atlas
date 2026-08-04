"""Checkpoint de lotes (resumable batches) en la extracción batched.

Cubre las funciones puras de persistencia/lectura de lotes y el comportamiento
de reanudación de ``_extract_marker_batched`` sin torch/marker/fitz: se
monkeypatchean ``page_count``, ``slice_pdf`` y ``_run_marker`` para simular la
extracción por lotes y verificar que una corrida cortada retoma desde el primer
lote faltante sin re-procesar los ya persistidos.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from atlas_local import extract as ex
from atlas_local.extract import (
    Extractor,
    _batch_stem,
    _read_batch_images,
    _read_batches,
    _write_batch,
)


# ── funciones puras de checkpoint ────────────────────────────────────────────
def test_batch_stem_zero_padded_and_ordered():
    # El zero-pad hace que el orden lexicográfico coincida con el numérico.
    stems = [_batch_stem(s, s + 39) for s in (1, 41, 401, 4001)]
    assert stems == sorted(stems)
    assert stems[0] == "p00001-p00040"


def test_write_then_read_roundtrip(tmp_path: Path):
    _write_batch(tmp_path, 1, 40, "md-uno", {"_page_0_Figure_1.png": b"IMG"})
    _write_batch(tmp_path, 41, 80, "md-dos", {})
    batches = _read_batches(tmp_path)
    assert batches == {(1, 40): "md-uno", (41, 80): "md-dos"}
    imgs = _read_batch_images(tmp_path)
    assert imgs == {"_page_0_Figure_1.png": b"IMG"}


def test_read_batches_missing_dir_is_empty(tmp_path: Path):
    assert _read_batches(tmp_path / "nope") == {}
    assert _read_batch_images(tmp_path / "nope") == {}


def test_read_batches_ignores_tmp_and_junk(tmp_path: Path):
    # Un .md.tmp de un corte a mitad de escritura no cuenta como lote válido.
    _write_batch(tmp_path, 1, 40, "ok", {})
    (tmp_path / "p00041-p00080.md.tmp").write_text("truncado", encoding="utf-8")
    (tmp_path / "otro.md").write_text("ruido", encoding="utf-8")
    assert _read_batches(tmp_path) == {(1, 40): "ok"}


def test_write_batch_is_atomic_no_tmp_left(tmp_path: Path):
    _write_batch(tmp_path, 1, 40, "x", {})
    assert list(tmp_path.glob("*.tmp")) == []
    assert (tmp_path / "p00001-p00040.md").exists()


# ── reanudación de _extract_marker_batched ───────────────────────────────────
class _FakeExtractor(Extractor):
    """Extractor que no toca marker: registra qué slices se le pidieron."""

    def __init__(self):
        self.calls: list[tuple[int, int]] = []

    def _run_marker(self, slice_path: Path):
        # El nombre del slice es "<stem>_p{start}-p{end}.pdf"; recuperamos el rango.
        name = slice_path.stem  # sin .pdf
        rng = name.rsplit("_p", 1)[1]  # "1-p40"
        start = int(rng.split("-p")[0])
        end = int(rng.split("-p")[1])
        self.calls.append((start, end))
        # marker emite numeración local (0-indexada) por slice.
        return f"{{0}}-----\nbody p{start}-p{end}", {}


@pytest.fixture
def _patch_pdfslice(monkeypatch):
    monkeypatch.setattr(ex, "_page_count", lambda pdf: 100)

    import atlas_local.pdfslice as ps

    monkeypatch.setattr(ps, "page_count", lambda pdf: 100)
    monkeypatch.setattr(ps, "slice_pdf", lambda src, s, e, out: Path(out).write_bytes(b"") or Path(out))


def test_fresh_run_processes_all_batches(tmp_path: Path, _patch_pdfslice):
    partial = tmp_path / "doc.partial"
    exx = _FakeExtractor()
    result = exx._extract_marker_batched(
        Path("doc.pdf"), batch_pages=40, partial_dir=partial
    )
    # 100 páginas / 40 → lotes [1-40], [41-80], [81-100].
    assert exx.calls == [(1, 40), (41, 80), (81, 100)]
    # Cada lote quedó persistido.
    assert set(_read_batches(partial)) == {(1, 40), (41, 80), (81, 100)}
    # El markdown global está en orden de página.
    assert result.markdown.index("p1-p40") < result.markdown.index("p41-p80") < result.markdown.index("p81-p100")


def test_resume_skips_persisted_batches(tmp_path: Path, _patch_pdfslice):
    partial = tmp_path / "doc.partial"
    # Simulamos una corrida previa que completó los dos primeros lotes.
    _write_batch(partial, 1, 40, "{40}-----\nviejo p1-p40", {})
    _write_batch(partial, 41, 80, "{80}-----\nviejo p41-p80", {})

    exx = _FakeExtractor()
    result = exx._extract_marker_batched(
        Path("doc.pdf"), batch_pages=40, partial_dir=partial
    )
    # Solo se re-procesa el lote faltante.
    assert exx.calls == [(81, 100)]
    # El resultado reensambla los lotes viejos + el nuevo, en orden.
    assert "viejo p1-p40" in result.markdown
    assert "viejo p41-p80" in result.markdown
    assert "body p81-p100" in result.markdown
    assert result.markdown.index("p1-p40") < result.markdown.index("p81-p100")


def test_no_partial_dir_still_works(tmp_path: Path, _patch_pdfslice):
    # Sin checkpoint (partial_dir=None): comportamiento clásico, nada en disco.
    exx = _FakeExtractor()
    result = exx._extract_marker_batched(Path("doc.pdf"), batch_pages=40)
    assert exx.calls == [(1, 40), (41, 80), (81, 100)]
    assert "p1-p40" in result.markdown
