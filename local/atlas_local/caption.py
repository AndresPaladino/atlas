"""Captions de figuras vía un VLM local (Qwen2.5-VL) servido por Ollama.

Las gráficas no se "OCRean": se *describen* con visión, para que su contenido
quede como texto que el wiki pueda capturar. Gated por tier y por la presencia
de Ollama; si algo falla, devolvemos el markdown sin tocar (degradación suave).
"""

from __future__ import annotations

import re

_PROMPT = (
    "Sos un asistente que describe figuras de material académico de ingeniería. "
    "Describí esta figura en 1-3 oraciones, en español, enfocándote en qué "
    "representa y qué información transmite (ejes, curvas, relaciones, valores "
    "clave). No inventes datos que no se vean. Sé conciso."
)


def caption_images(images: dict[str, bytes], model: str) -> dict[str, str]:
    """Devuelve {nombre_imagen: caption}. Errores → se omite esa figura."""
    import ollama

    out: dict[str, str] = {}
    for name, data in images.items():
        try:
            resp = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": _PROMPT, "images": [data]}],
            )
            text = (resp.get("message", {}) or {}).get("content", "").strip()
            if text:
                out[name] = text
        except Exception:
            continue
    return out


def inline_captions(markdown: str, captions: dict[str, str]) -> str:
    """Inserta cada caption como blockquote justo después de su ref de imagen.

    marker emite refs tipo ``![](nombre.png)``. Para cada figura con caption,
    agregamos ``> **Figura:** …`` debajo. Las imágenes en sí quedan locales
    (gitignored); el caption-texto viaja en el .md.
    """
    for name, caption in captions.items():
        pattern = re.compile(r"(!\[[^\]]*\]\(\s*" + re.escape(name) + r"\s*\))")
        replacement = r"\1\n\n> **Figura:** " + caption.replace("\\", "\\\\")
        markdown, n = pattern.subn(replacement, markdown, count=1)
        if n == 0:
            # No se encontró la ref (marker pudo no incrustarla): append al final.
            markdown += f"\n\n> **Figura ({name}):** {caption}\n"
    return markdown
