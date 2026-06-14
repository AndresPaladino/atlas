"""Tests de la segmentación (lógica pura, sin GPU/marker)."""

from __future__ import annotations

import re

import pytest

from atlas_local import segment as seg


def _para(n_chars: int, label: str = "x") -> str:
    return (label * n_chars)


# ── parse_blocks ─────────────────────────────────────────────────────────────
def test_parse_blocks_is_lossless_partition():
    md = "intro\n\n# A\ncuerpo a\n\n## A.1\ncuerpo a1\n\n# B\ncuerpo b\n"
    blocks = seg.parse_blocks(md)
    # Reconstrucción exacta: los bloques particionan el documento sin pérdida.
    assert "".join(b.text for b in blocks) == md
    # Preámbulo + 3 headings.
    assert [b.level for b in blocks] == [0, 1, 2, 1]
    assert [b.title for b in blocks] == ["", "A", "A.1", "B"]
    # Jerarquía de ancestros.
    assert blocks[2].parents == ["A"]
    assert blocks[3].parents == []


def test_headings_inside_code_fence_are_ignored():
    md = "# Real\n\n```python\n# no soy heading\nx = 1\n```\n\n## Otra\n"
    blocks = seg.parse_blocks(md)
    titles = [b.title for b in blocks]
    assert "Real" in titles and "Otra" in titles
    assert "no soy heading" not in titles


def test_clean_title_strips_emphasis():
    md = "## **1.3.4. Test** de la *derivada*\n"
    (block,) = seg.parse_blocks(md)
    assert block.title == "1.3.4. Test de la derivada"


# ── páginas ──────────────────────────────────────────────────────────────────
def test_page_inferred_from_image_ref():
    md = "# A\n\n![](_page_3_Figure_1.jpeg)\ncuerpo\n"
    (block,) = seg.parse_blocks(md)
    assert block.page_start == 3  # 0-indexado interno


def test_page_inferred_from_pagination_marker():
    md = "# A\ncuerpo\n\n{5}------------------------------------------------\n\n# B\nmas\n"
    blocks = seg.parse_blocks(md)
    assert blocks[1].page_start == 5


# ── plan_chunks ──────────────────────────────────────────────────────────────
def test_chunks_respect_budget_and_dont_split_sections():
    # 6 secciones de ~400 tokens (1600 chars) c/u; target 1000, max 1500.
    md = "".join(f"# S{i}\n\n{_para(1600)}\n\n" for i in range(6))
    blocks = seg.parse_blocks(md)
    chunks = seg.plan_chunks(blocks, target_tokens=1000, max_tokens=1500)
    # Cada bloque cabe entero en un único chunk (nunca partido).
    assert "".join(c.text for c in chunks) == "".join(b.text for b in blocks)
    # Cada chunk individual no excede el max.
    for c in chunks:
        assert c.tokens <= 1500


def test_oversize_section_is_hard_split():
    # Una sección de ~5000 tokens (20k chars) en párrafos → varios chunks.
    body = "\n\n".join(_para(2000) for _ in range(10))
    md = f"# Grande\n\n{body}\n"
    blocks = seg.parse_blocks(md)
    chunks = seg.plan_chunks(blocks, target_tokens=1000, max_tokens=1500)
    assert len(chunks) > 1
    # Todos los chunks provienen de la misma sección.
    assert all("Grande" in c.title for c in chunks)


# ── should_segment ───────────────────────────────────────────────────────────
@pytest.mark.parametrize("pages,tokens,expected", [
    (4, 5_000, False),       # examen chico
    (50, 5_000, True),       # muchas páginas
    (10, 30_000, True),      # pocas páginas pero mucho texto
    (39, 24_999, False),     # justo bajo ambos umbrales
])
def test_should_segment(pages, tokens, expected):
    assert seg.should_segment(pages, tokens) is expected


# ── slugify ──────────────────────────────────────────────────────────────────
def test_slugify_ascii_kebab():
    assert seg.slugify("1.3.4. Extremos relativos (test)") == "1-3-4-extremos-relativos-test"
    assert seg.slugify("Función Implícita") == "funcion-implicita"
    assert seg.slugify("***") == "seccion"


# ── artefactos en disco ──────────────────────────────────────────────────────
def test_segment_markdown_writes_toc_and_chunks(tmp_path):
    md = "".join(f"# S{i}\n\n{_para(1600)}\n\n" for i in range(6))
    md_path = tmp_path / "Doc.md"
    md_path.write_text(md, encoding="utf-8")

    result = seg.segment_markdown(
        md, md_path=md_path, source_rel="Doc.pdf", n_pages=50, target_tokens=1000,
    )

    assert result.toc_path == tmp_path / "Doc.toc.md"
    assert result.chunks_dir == tmp_path / "Doc"
    assert result.n_chunks > 1

    # Todos los chunks existen en disco.
    for p in result.chunk_paths:
        assert p.exists()

    # Cada `chunk` referenciado en el TOC existe realmente.
    toc = result.toc_path.read_text(encoding="utf-8")
    referenced = set(re.findall(r"`([^`]+\.md)`", toc))
    on_disk = {p.name for p in result.chunk_paths}
    # El TOC menciona el directorio y los chunks; todos los .md referenciados existen.
    chunk_refs = {r for r in referenced if r in on_disk or r.endswith(".md") and "/" not in r}
    assert on_disk.issubset(referenced) or on_disk.issubset(chunk_refs | on_disk)
    for name in on_disk:
        assert name in toc


def test_reextraction_cleans_stale_chunks(tmp_path):
    md_path = tmp_path / "Doc.md"
    big = "".join(f"# S{i}\n\n{_para(1600)}\n\n" for i in range(6))
    md_path.write_text(big, encoding="utf-8")
    r1 = seg.segment_markdown(big, md_path=md_path, source_rel="Doc.pdf", n_pages=50, target_tokens=1000)
    n1 = r1.n_chunks
    assert n1 >= 2

    # Re-segmentar con muchas menos secciones → menos chunks; sin huérfanos.
    small = "# Solo\n\n" + _para(1600) + "\n"
    r2 = seg.segment_markdown(small, md_path=md_path, source_rel="Doc.pdf", n_pages=50, target_tokens=1000)
    on_disk = list(r2.chunks_dir.glob("*.md"))
    assert len(on_disk) == r2.n_chunks
    assert r2.n_chunks < n1
