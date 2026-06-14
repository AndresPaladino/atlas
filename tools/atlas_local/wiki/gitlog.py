"""Log de mutaciones del wiki, derivado de ``git`` — no mantenido a mano.

La mutación real del wiki **es** el commit. ``wiki/log.md`` dejaba de
sincronizarse apenas alguien tocaba un archivo; ``git log`` siempre es fiel.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def render_log(repo_root: Path, limit: int = 30) -> str:
    """Renderiza el historial de ``wiki/`` como markdown legible."""
    try:
        r = subprocess.run(
            ["git", "log", f"-{limit}", "--date=short",
             "--format=## [%ad] %s%n%n- %h por %an", "--", "wiki/"],
            cwd=repo_root, capture_output=True, text=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"(no se pudo leer git log: {exc})"
    if r.returncode != 0:
        return f"(git log falló: {r.stderr.strip()})"
    out = r.stdout.strip()
    return out or "(sin commits que toquen wiki/ todavía)"
