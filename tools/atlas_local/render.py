"""Filtro best-effort LaTeX→Unicode para leer mate en terminal cruda.

No es un render vivo (Claude Code no expone un hook que reescriba la salida del
asistente): es un filtro que se corre sobre texto ya guardado — p.ej. una
respuesta archivada al wiki. Convierte los spans ``$…$`` y ``$$…$$`` a Unicode
aproximado; la prosa queda intacta. Para fidelidad total, leer en un cliente con
render de KaTeX.
"""

from __future__ import annotations

import re

# $$ … $$ (bloque) y $ … $ (inline). El bloque primero para no romperlo.
_BLOCK = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_INLINE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", re.DOTALL)


def _latex_to_unicode(latex: str) -> str:
    try:
        from pylatexenc.latex2text import LatexNodes2Text

        return LatexNodes2Text().latex_to_text(latex).strip()
    except Exception:
        return latex.strip()  # sin pylatexenc: dejar el LaTeX literal


def render_text(text: str) -> str:
    """Reemplaza la mate delimitada por su aproximación Unicode."""
    text = _BLOCK.sub(lambda m: "\n    " + _latex_to_unicode(m.group(1)) + "\n", text)
    text = _INLINE.sub(lambda m: _latex_to_unicode(m.group(1)), text)
    return text
