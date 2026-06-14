#!/usr/bin/env python3
"""PreToolUse hook (Read) — enforcement del firewall de /practice.

Claude Code invoca este script antes de cada Read, pasando el tool input por
stdin. Si hay una sesión practice activa (estado en `.atlas/session.json`) y el
archivo está bloqueado, devolvemos exit 2 con el motivo en stderr → Claude Code
**deniega** la lectura. El firewall deja de depender de que el modelo obedezca.

Falla *abierto*: si `atlas` no está disponible o algo sale mal, permitimos la
lectura (exit 0) para no romper el flujo normal.
"""

from __future__ import annotations

import json
import subprocess
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = (data.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return 0

    try:
        r = subprocess.run(
            ["atlas", "session", "check", file_path],
            capture_output=True, text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return 0  # atlas no instalado / no en PATH → fail-open

    if r.returncode == 2:
        sys.stderr.write((r.stdout or r.stderr).strip() + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
