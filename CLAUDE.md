# Atlas — router

Atlas es un sistema de estudio personal para ingeniería. Este archivo es el **dispatcher**: dice qué leer y en qué orden. Todo el comportamiento concreto vive en `schema/`.

## Al iniciar una sesión

Leé, en este orden:

1. `profile/student_profile.md` — materias activas y preferencias.
2. `schema/modes.md` — los 4 modos, default heurístico, firewall.

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

## Bloom — referencia

| Nivel | Descriptor | Qué puede hacer el estudiante |
|-------|-----------|-------------------------------|
| 1 | Inicial | Reconoce el concepto, no puede aplicarlo solo |
| 2 | Comprensión | Explica con sus palabras |
| 3 | Aplicación | Resuelve ejercicios tipo con guía |
| 4 | Análisis | Identifica qué herramienta usar sin que se lo digan |
| 5 | Síntesis | Combina conceptos para resolver problemas nuevos |
| 6 | Evaluación | Puede enseñarlo y detectar errores en soluciones ajenas |

La fuente única de verdad del Bloom de cada concepto es el campo `bloom:` en su página `wiki/`. Las materias proyectan vía Dataview. Detalles en `schema/wiki-conventions.md`.

## Estructura

```
profile/        ← perfil del estudiante
schema/         ← reglas (modes + 4 protocolos + wiki-conventions + output-conventions)
.claude/commands/  ← adapters de slash commands
wiki/           ← grafo de conocimiento (LLM-owned)
raw/            ← fuentes inmutables (human-archived) + .md extraídos por atlas-local
local/          ← pipeline de extracción local (PDF→markdown, GPU). Ver local/README.md
subjects/       ← una entrada por materia
archive/        ← materias finalizadas (local, no en git)
logs/           ← logs por mes (local, no en git)
```
