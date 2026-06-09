# Atlas

Sistema de estudio personal para ingeniería, construido sobre [Claude Code](https://claude.ai/code).

Atlas organiza el cursado por materia, guía las sesiones de práctica con método Socrático, lleva un registro automático del progreso usando la taxonomía de Bloom, y mantiene un **wiki interconectado** (`wiki/`) que acumula conocimiento a través de sesiones y materias.

---

## Cómo funciona

Abrís este repositorio en Claude Code. El agente lee `CLAUDE.md` (router) y sabe cómo dispatcher: `CLAUDE.md` apunta a `schema/modes.md`, que define los 4 modos de operación.

```
PDFs (raw/) ──[atlas-local, GPU local]──→ raw/*.md (LaTeX + captions)
                                              │
sources (raw/)  ──/ingest──→  wiki/  ──/query──→  respuesta con citas
                              ↑↓ Bloom
                              subjects/
                              ↑
                           /practice (Socrático, con firewall sobre wiki)

                           /lint  ──→  auditoría de consistencia
```

> **Capa de extracción local** (`local/`): un CLI (`atlas-local`) convierte los
> PDFs a markdown con LaTeX y captions de figuras usando la GPU disponible
> (CUDA/MPS/CPU), *antes* del `/ingest`. Claude lee ese texto barato en vez de la
> imagen de cada página → menos tokens, misma fidelidad. Ver `local/README.md`.

---

## Los 4 modos

| Modo | Comando | Para qué sirve |
|---|---|---|
| Ingest | `/ingest [ruta]` | Cargar un PDF, libro o nota cruda al wiki. La LLM crea/actualiza páginas, aristas y log. |
| Query | `/query <pregunta>` | Pregunta abierta. La LLM consulta el wiki, responde con `[[wikilinks]]` + citas, y ofrece archivar la respuesta. |
| Practice | `/practice [tema]` | Sesión Socrática estricta. Pista mínima, nunca solución. **Firewall**: la LLM no puede leer páginas wiki del tema activo, para no filtrar el camino. |
| Lint | `/lint [scope]` | Auditoría: orphans, links rotos, Bloom desincronizado, fuentes sin ingest, frontmatter incompleto. |

Sin slash command, Atlas elige modo según heurística: si el mensaje describe un ejercicio → `/practice`; si pide explicación → `/query`. Documentado en `schema/modes.md`.

Todo el comportamiento concreto vive en `schema/`. `CLAUDE.md` es solo el router de entrada (~40 líneas).

---

## Estructura

```
atlas/
├── CLAUDE.md                ← router de entrada (~40 líneas)
├── README.md                ← este archivo
├── setup.sh                 ← scaffolding inicial
├── profile/
│   └── student_profile.md   ← carrera, materias activas, preferencias
├── schema/                  ← reglas neutrales del sistema (portable)
│   ├── modes.md             ← dispatcher de modos + default + firewall
│   ├── wiki-conventions.md  ← contrato del wiki (tipos, frontmatter, notación)
│   ├── ingest-protocol.md
│   ├── query-protocol.md
│   ├── practice-protocol.md ← reglas Socráticas + firewall (no negociable)
│   └── lint-protocol.md
├── .claude/
│   └── commands/            ← slash commands (adapters thin)
├── wiki/                    ← grafo de conocimiento (LLM-owned)
│   ├── index.md
│   ├── log.md
│   ├── README.md
│   ├── areas/               ← 5 MOCs (math, signals, computing, eng-physics, ml)
│   ├── concepts/
│   ├── theorems/
│   ├── methods/
│   ├── examples/
│   ├── comparisons/
│   └── sources/             ← resúmenes de PDFs/libros con mapa de coverage
├── raw/                     ← fuentes inmutables (PDFs, etc — gitignored)
├── subjects/                ← una entrada por materia
│   ├── _template/index.md
│   └── [materia]/index.md   ← temario, Bloom, log + sección "Conceptos wiki" Dataview
├── archive/                 ← materias finalizadas (local, no en git)
└── logs/                    ← logs por mes (local, no en git)
```

---

## El firewall (modo `/practice`)

El modo Socrático es la pieza más sensible: si la LLM puede leer libremente el wiki del tema que el estudiante está intentando, filtra la solución. Atlas resuelve esto con un firewall estructural:

> Durante `/practice` sobre tema **T**, está prohibido leer `wiki/concepts/`, `wiki/theorems/`, `wiki/methods/`, `wiki/examples/` con tag/alias = T.

Se permite leer `wiki/areas/*.md` (mapas de alto nivel), listar nombres sin abrir contenido, y leer páginas de otros temas (para conectar). Detalles en `schema/practice-protocol.md`.

---

## Portabilidad

El wiki está diseñado para sobrevivir fuera de Claude Code:

- **Datos** (`wiki/`, `subjects/`, `profile/`): markdown + YAML + `[[wikilinks]]`. Funcionan en Obsidian, VS Code, o cualquier parser markdown estándar.
- **Protocolos** (`schema/*.md`): lenguaje neutral, sirven como system prompts para cualquier LLM.
- **Adapter** (`.claude/commands/*.md` + `CLAUDE.md`): única parte Claude-Code-específica. Trivial de re-implementar para otra UI.

Hoy hay dos interfaces de primera clase sobre los mismos archivos: Claude Code y Obsidian (graph view + Dataview).

---

## Setup

### Requisitos
- [Claude Code](https://claude.ai/code) instalado
- (Opcional) Obsidian + plugin **Dataview** si querés graph view y proyecciones automáticas

### Instalación

```bash
git clone https://github.com/TU_USUARIO/atlas.git
cd atlas
bash setup.sh
```

`setup.sh` hace:
1. Crea `.claude/settings.local.json` desde el ejemplo.
2. Crea el directorio de logs del mes actual.
3. Scaffolea `raw/{lectures/...,books,papers,notes-import,assets}/`.
4. Scaffolea `wiki/{concepts,theorems,methods,examples,comparisons,sources}/`.

---

## Agregar una materia

```bash
cp subjects/_template/index.md subjects/[nombre-materia]/index.md
```

Luego:
1. Editá `subjects/[nombre-materia]/index.md` con el temario y la notación del curso.
2. Agregá la materia a `profile/student_profile.md` bajo "Materias activas".

A medida que hagas `/ingest` o `/practice` sobre la materia, las páginas wiki creadas con `seen_in_subjects: [nombre-materia]` aparecerán automáticamente en la sección "Conceptos wiki" del índice de la materia.

---

## Comenzar una sesión

```bash
claude
```

El agente lee `CLAUDE.md` → `schema/modes.md`. Decile qué querés trabajar y empieza la sesión.

- Si tipeás un slash command (`/ingest`, `/query`, `/practice`, `/lint`) activa ese modo directo.
- Si no, aplica la heurística default: ejercicio → `/practice`, pregunta → `/query`, fuente → `/ingest`.

Anuncia el modo en su primer mensaje: `[modo: practice]`.

---

## Al cerrar una sesión

Según el modo:

- **`/practice`**: actualiza tabla "Sesiones con Claude" en `subjects/[materia]/index.md`, sube/baja `bloom:` de páginas wiki tocadas, append a `wiki/log.md`.
- **`/ingest` y `/query`** (con file-back): crean/modifican páginas wiki, append a `wiki/log.md`.
- **`/lint`**: append a `wiki/log.md` por cada fix aplicado.

---

## Personalización

- Cambiar el idioma o el tono Socrático: editar `schema/practice-protocol.md`.
- Modificar las reglas de cada modo: editar `schema/<modo>-protocol.md`.
- Cambiar la heurística default: editar `schema/modes.md`.
- Ajustar convenciones del wiki (frontmatter, notación, naming): `schema/wiki-conventions.md`.

`CLAUDE.md` casi no se toca — es solo el router.

---

## Licencia

MIT — libre para usar, adaptar y compartir.
