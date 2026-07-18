"""Estado de sesión de Atlas — la base del firewall *enforced*.

Vive en ``.atlas/session.json`` (gitignored). Guarda el modo activo, el tema T
de una sesión ``/practice``, los slugs bloqueados (calculados desde el grafo) y
la válvula ``reveal``. Sobrevive a la compactación de contexto: el firewall deja
de depender de que el modelo "recuerde" qué no leer.

El hook ``PreToolUse`` invoca :func:`check_read` para denegar lecturas de verdad.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .loader import Page, load_wiki, normalize_slug

SESSION_REL = ".atlas/session.json"


@dataclass
class Session:
    mode: str = "query"               # query | learn | practice | ingest | lint
    topic: str | None = None          # T, solo en practice
    blocked_slugs: list[str] = field(default_factory=list)
    reveal: bool = False              # válvula de escape one-shot

    def as_dict(self) -> dict:
        return asdict(self)


def _session_path(root: Path) -> Path:
    return root / SESSION_REL


def load_session(root: Path) -> Session:
    path = _session_path(root)
    if not path.exists():
        return Session()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return Session()
    return Session(
        mode=data.get("mode", "query"),
        topic=data.get("topic"),
        blocked_slugs=list(data.get("blocked_slugs", [])),
        reveal=bool(data.get("reveal", False)),
    )


def save_session(root: Path, session: Session) -> None:
    path = _session_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(session.as_dict(), indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


# ── cálculo de slugs bloqueados (firewall por grafo) ──────────────────────────
def _matches_topic(page: Page, topic: str) -> bool:
    t = topic.strip().lower()
    haystacks = [page.slug, str(page.frontmatter.get("title", ""))]
    haystacks += [str(a) for a in page.aliases]
    haystacks += [str(tag) for tag in page.tags]
    return any(t in h.lower() for h in haystacks)


def compute_blocked(wiki_dir: Path, topic: str) -> list[str]:
    """Slugs a bloquear para el tema T: las páginas sobre T **más su vecindario**
    ``requires``/``unlocks`` (1 hop). Resuelve el blast-radius ad-hoc del firewall
    viejo: un prerrequisito sin el tag ya no queda legible y filtra estructura."""
    pages = load_wiki(wiki_dir)
    direct = [p for p in pages if _matches_topic(p, topic)]
    blocked: set[str] = {p.slug for p in direct}
    for p in direct:
        blocked.update(p.edge("requires"))
        blocked.update(p.edge("unlocks"))
        # ejemplos que ilustran una página sobre T también se bloquean
    for p in pages:
        if any(normalize_slug(x) in blocked for x in p.edge("illustrates")):
            blocked.add(p.slug)
    return sorted(blocked)


def set_practice(root: Path, wiki_dir: Path, topic: str) -> Session:
    session = Session(
        mode="practice", topic=topic,
        blocked_slugs=compute_blocked(wiki_dir, topic), reveal=False,
    )
    save_session(root, session)
    return session


def set_mode(root: Path, mode: str) -> Session:
    session = load_session(root)
    session.mode = mode
    if mode != "practice":
        session.topic = None
        session.blocked_slugs = []
        session.reveal = False
    save_session(root, session)
    return session


def set_reveal(root: Path, value: bool = True) -> Session:
    session = load_session(root)
    session.reveal = value
    save_session(root, session)
    return session


def clear(root: Path) -> Session:
    session = Session()
    save_session(root, session)
    return session


# ── decisión del hook ─────────────────────────────────────────────────────────
def check_read(root: Path, target: Path) -> tuple[bool, str]:
    """¿Se permite leer ``target``? (allowed, motivo).

    Deniega si hay sesión practice activa sin reveal y el target es una página
    bloqueada o cae bajo raw/. En cualquier otro caso, permite.
    """
    session = load_session(root)
    if session.mode != "practice" or session.reveal:
        return True, ""
    try:
        rel = target.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return True, ""  # fuera del repo: no es asunto del firewall

    if rel.startswith("raw/") or rel.startswith("extracted/"):
        return False, f"firewall /practice (T={session.topic}): raw/ y extracted/ están bloqueados"
    if rel.startswith("wiki/"):
        slug = Path(rel).stem
        if slug in session.blocked_slugs:
            return False, (
                f"firewall /practice (T={session.topic}): [[{slug}]] está bloqueado. "
                f"Salí con /query o confirmá /reveal para verlo."
            )
    return True, ""
