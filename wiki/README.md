---
type: readme
updated: 2026-06-02
---

# Wiki — cómo navegarlo

Este directorio es el **grafo de conocimiento** de Atlas. Cada archivo es un concepto, teorema, método, ejemplo, comparación o fuente. Los archivos están conectados por `[[wikilinks]]` y por aristas `requires:` / `unlocks:` en el frontmatter.

## Carpetas

```
wiki/
├── index.md          ← catálogo: empezá acá
├── log.md            ← append-only: qué cambió y cuándo
├── areas/            ← 5 MOCs por área (math, signals, computing, eng-physics, ml)
├── concepts/         ← ideas / objetos / entidades
├── theorems/         ← enunciados con hipótesis y conclusión
├── methods/          ← procedimientos
├── examples/         ← casos resueltos
├── comparisons/      ← contrastes entre 2+ entidades
└── sources/          ← resúmenes de PDFs / libros / papers con mapa de coverage
```

## En Obsidian

1. Abrir Atlas como vault.
2. Habilitar plugins: **Dataview** (proyecciones), **Templater** opcional.
3. Graph view: filtrar por `path:wiki` para ver solo el grafo conceptual sin `subjects/`.

Los bloques Dataview en `index.md`, `areas/*.md` y en las secciones "Conceptos wiki" de cada `subjects/[materia]/index.md` se renderizan automáticamente.

## En cualquier editor

El wiki es markdown puro. Los wikilinks son legibles aunque no naveguen automáticamente. El frontmatter es YAML estándar.

## Convenciones

Ver `schema/wiki-conventions.md` para el contrato completo: tipos, frontmatter, notación KaTeX, citas, naming.

## Modificaciones

El wiki se modifica únicamente vía los 4 modos (`/ingest`, `/query`, `/practice`, `/lint`). Edición manual está permitida pero el log se desincroniza — preferir los modos.
