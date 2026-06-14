"""Reindexado de páginas/imágenes al concatenar lotes en extracción batched.

Solo cubre la lógica pura de offset (sin torch/marker/fitz): que al pegar slices
los separadores de página y los nombres de imagen queden en la numeración global
del documento, que es de lo que depende la segmentación.
"""

from __future__ import annotations

from atlas_local.extract import _offset_image_names, _offset_page_numbers


def test_offset_zero_is_noop():
    md = "{0}-----\ntexto\n![](_page_0_Figure_1.png)"
    assert _offset_page_numbers(md, 0) == md
    imgs = {"_page_0_Figure_1.png": b"x"}
    assert _offset_image_names(imgs, 0) == imgs


def test_offset_page_markers():
    md = "{0}--------\nuno\n{1}--------\ndos"
    out = _offset_page_numbers(md, 40)
    assert "{40}--------" in out
    assert "{41}--------" in out
    assert "{0}" not in out


def test_offset_image_refs_in_markdown():
    md = "![](_page_0_Figure_1.png) y _page_2_Picture_0.jpeg"
    out = _offset_page_numbers(md, 40)
    assert "_page_40_Figure_1.png" in out
    assert "_page_42_Picture_0.jpeg" in out


def test_offset_image_keys_match_markdown():
    offset = 40
    imgs = {"_page_0_Figure_1.png": b"a", "_page_1_Picture_0.png": b"b"}
    out = _offset_image_names(imgs, offset)
    assert set(out) == {"_page_40_Figure_1.png", "_page_41_Picture_0.png"}
    # Las claves renombradas coinciden con las refs reescritas en el markdown.
    md = "![](_page_0_Figure_1.png) ![](_page_1_Picture_0.png)"
    md_out = _offset_page_numbers(md, offset)
    for name in out:
        assert name in md_out


def test_only_first_page_number_is_offset():
    # El nº de figura (último grupo) no se toca; solo el de página.
    md = "_page_3_Figure_7.png"
    assert _offset_page_numbers(md, 10) == "_page_13_Figure_7.png"
