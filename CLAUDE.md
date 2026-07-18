# Atlas — router

Atlas es un sistema personal de conocimiento e interacción con él. Este archivo es el **dispatcher**: dice qué leer y en qué orden. Todo el comportamiento concreto vive en `schema/`.

## Al iniciar una sesión

Leé `schema/modes.md` — los 5 modos, default heurístico, firewall.

No leas más cosas hasta saber qué modo activar.

## Modos

Cinco modos: `/ingest`, `/query`, `/learn`, `/practice`, `/lint`. La tabla completa (comando → protocolo → propósito) y la heurística default viven en `schema/modes.md` — single source of truth.

Si no hay slash command, aplicá la heurística default de `schema/modes.md` (cierra hacia `/practice` ante ambigüedad).

**Anuncio de modo (regla canónica):** anunciá el modo activado al inicio de tu primera respuesta: `"[modo: X]"`. Esta es la única definición; los protocolos no la repiten.

Una vez identificado el modo, leé el protocolo correspondiente y aplicalo.

## Idioma

Español. Términos técnicos en inglés son aceptables.

## Preferencias de interacción

- Socrático puro en práctica: nunca dar solución directa. El usuario tipea sus pasos; el agente evalúa y da pista mínima si está trabado.
- Ejemplos concretos antes de abstracción.

## Backend determinístico (`atlas` CLI)

La lógica que no es juicio del LLM vive en código testeado (`tools/`), no en prompts:

- `atlas validate` — valida el contrato de frontmatter.
- `atlas lint [scope] --json` — checks de grafo (orphans, links/aristas rotos, simetría…).
- `atlas index` — regenera `wiki/index.md` y los MOCs desde el FS (cero drift).
- `atlas log` — log de mutaciones derivado de git.
- `atlas session …` — estado de modo/firewall que el hook `PreToolUse` enforcea.
- `atlas forget <fuente>` — olvida una fuente preservando entidades compartidas.
- `atlas ingest-status` / `atlas ingest-stamp <fuente>` — hash raw→wiki para saltear re-ingestas (consumido por `/ingest --compile`).

Los protocolos llaman a estos comandos; no reimplementan la detección.

## Estructura

```
schema/            ← reglas (modes + 4 protocolos + wiki-conventions + output-conventions + purpose: qué/para qué)
.claude/commands/  ← adapters de slash commands (incluye /reveal: válvula del firewall)
.claude/hooks/     ← firewall_read.py (PreToolUse) enforcea el firewall de /practice
wiki/              ← grafo de conocimiento; index/MOCs GENERADOS por `atlas index`
raw/               ← fuentes inmutables (human-archived) + .md extraídos por atlas
tools/             ← CLI: backend del wiki (validate/lint/index/session) + extracción PDF. Ver tools/README.md
```
## Convenciones
Por mas de que estes en un entorno windows intenta usar wsl para ejecutar comandos de terminal. 