---
description: Auditar consistencia del wiki (orphans, links/aristas rotos, frontmatter, drift)
---

Activá modo `lint`. Corré `atlas session mode lint` (levanta el firewall si venías de
`/practice`). Antes de responder, leé `schema/lint-protocol.md`.

Scope (opcional, vacío = todo el wiki): $ARGUMENTS

1. Corré `atlas lint $ARGUMENTS --json` (o sin scope si está vacío). La **detección**
   es determinística y vive en el CLI — no la reimplementes leyendo archivos a mano.
2. Presentá el reporte resumido al usuario a partir del JSON.
3. Ofrecé fix interactivo finding por finding (read-only por default; no modifiques
   nada sin confirmación explícita por cada uno).
4. Si aplicás fixes que tocan el catálogo, corré `atlas index` al cerrar.
