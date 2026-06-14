from __future__ import annotations

from atlas_local.wiki.loader import load_wiki, split_frontmatter


def test_split_frontmatter_ok():
    fm, err, body, offset = split_frontmatter("---\ntype: concept\nx: 1\n---\n\nhola\n")
    assert err is None
    assert fm == {"type": "concept", "x": 1}
    assert body.strip() == "hola"
    assert offset == 5


def test_split_frontmatter_none():
    fm, err, body, offset = split_frontmatter("# sin frontmatter\n")
    assert fm == {} and err is None and offset == 1


def test_split_frontmatter_unterminated():
    fm, err, _, _ = split_frontmatter("---\ntype: concept\nsin cierre\n")
    assert fm == {} and "cierre" in err


def test_split_frontmatter_bad_yaml():
    fm, err, _, _ = split_frontmatter("---\n: : :\n bad\n---\n\nbody")
    assert fm == {} and "YAML" in err


def test_links_and_edges(wiki):
    pages = {p.slug: p for p in load_wiki(wiki)}
    g = pages["gradient"]
    assert any(l.target == "greens-theorem" for l in g.links)
    assert g.edge("unlocks") == ["greens-theorem"]
    th = pages["greens-theorem"]
    assert th.edge("requires") == ["gradient"]
    assert th.aliases == ["Green"]
