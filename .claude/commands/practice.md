---
description: Sesión Socrática estricta (con firewall sobre wiki del tema activo)
---

Activá modo `practice`. Antes de responder, leé `schema/practice-protocol.md` y `schema/modes.md`.

Tema (puede estar vacío): $ARGUMENTS

1. Identificá el tema **T** según el protocolo (argumento → primer mensaje → preguntá).
2. Corré `atlas session set "<T>"`. Esto fija el estado de sesión y calcula los
   slugs bloqueados desde el grafo (la página de T **más** su vecindario
   `requires`/`unlocks`). El hook `PreToolUse` enforcea el firewall: ya no depende
   de que vos recuerdes no leer — un `Read` bloqueado es denegado por el sistema.
3. Anunciá `[modo: practice]` con T y los slugs bloqueados que reportó el comando.
4. Aplicá las reglas Socráticas. Si el usuario pide la respuesta: no cedas; ofrecé
   `/reveal` (válvula puntual) o `/query` (salir del modo).
