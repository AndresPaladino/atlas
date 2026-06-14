---
description: Cargar una fuente cruda al wiki
---

Activá modo `ingest`. Corré `atlas session mode ingest` (levanta el firewall si venías
de `/practice`). Antes de responder, leé `schema/ingest-protocol.md` y `schema/wiki-conventions.md`.

Argumento del usuario: $ARGUMENTS

- Si el argumento es `--compile` (o `compile`): ejecutá el modo compile del protocolo (sección "Modo compile"). Recordá: el ingest lee el `.md` cacheado en `raw/` (producido por `atlas extract`) si existe; el PDF visual es fallback.
- Si el argumento es una ruta de archivo en `raw/`: leerla y arrancar el flujo normal del protocolo.
- Si está vacío o es ambiguo: preguntá qué fuente vas a ingerir.

Al terminar de crear/actualizar páginas, corré `atlas index` (regenera catálogo y MOCs) y `atlas validate` (verifica el frontmatter). El commit es el registro de la mutación — no edites `wiki/log.md` a mano.
