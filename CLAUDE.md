# Atlas — router

Atlas es un sistema personal de conocimiento e interacción con él. Este archivo es el **dispatcher**: dice qué leer y en qué orden. Todo el comportamiento concreto vive en `schema/`.

## Al iniciar una sesión

Leé `schema/modes.md` — los 4 modos, default heurístico, firewall.

No leas más cosas hasta saber qué modo activar.

## Modos

| Modo | Comando | Protocolo |
|---|---|---|
| Ingest | `/ingest [ruta]` | `schema/ingest-protocol.md` |
| Query | `/query <pregunta>` | `schema/query-protocol.md` |
| Practice | `/practice [tema]` | `schema/practice-protocol.md` |
| Lint | `/lint [scope]` | `schema/lint-protocol.md` |

Si no hay slash command, aplicá la heurística default de `schema/modes.md` (cierra hacia `/practice` ante ambigüedad). Anunciá el modo activado en tu primera respuesta: `"[modo: X]"`.

Una vez identificado el modo, leé el protocolo correspondiente y aplicalo.

## Idioma

Español. Términos técnicos en inglés son aceptables.

## Preferencias de interacción

- Socrático puro en práctica: nunca dar solución directa. El usuario tipea sus pasos; el agente evalúa y da pista mínima si está trabado.
- Ejemplos concretos antes de abstracción.

## Estructura

```
schema/            ← reglas (modes + 4 protocolos + wiki-conventions + output-conventions)
.claude/commands/  ← adapters de slash commands
wiki/              ← grafo de conocimiento (LLM-owned)
raw/               ← fuentes inmutables (human-archived) + .md extraídos por atlas
tools/             ← CLI de extracción local (PDF→markdown, GPU). Ver tools/README.md
```
