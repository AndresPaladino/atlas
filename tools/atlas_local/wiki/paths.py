"""Localización de la raíz del repo y de ``wiki/`` desde cualquier cwd.

Reusa la misma heurística que ``cli.find_raw_dir``: subir hasta encontrar un
directorio que tenga ``schema/`` y ``wiki/``.
"""

from __future__ import annotations

import os
from pathlib import Path


def find_repo_root(explicit: Path | None = None) -> Path | None:
    if explicit is not None:
        return explicit.expanduser().resolve()
    env = os.environ.get("ATLAS_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    cur = Path.cwd().resolve()
    for base in (cur, *cur.parents):
        if (base / "schema").is_dir() and (base / "wiki").is_dir():
            return base
    return None


def find_wiki_dir(explicit: Path | None = None) -> Path | None:
    if explicit is not None:
        return explicit.expanduser().resolve()
    root = find_repo_root()
    return (root / "wiki") if root else None
