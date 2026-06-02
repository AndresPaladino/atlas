---
description: Cargar una fuente cruda al wiki
---

Activá modo `ingest`. Antes de responder, leé `schema/ingest-protocol.md` y `schema/wiki-conventions.md`.

Argumento del usuario: $ARGUMENTS

- Si el argumento es `--compile` (o `compile`): ejecutá el modo compile del protocolo (sección "Modo compile").
- Si el argumento es una ruta de archivo en `raw/`: leerla y arrancar el flujo normal del protocolo.
- Si está vacío o es ambiguo: preguntá qué fuente vas a ingerir.
