---
type: concept
title: "Estados de un proceso"
aliases: ["process states", "estado proceso", "transiciones de estado"]
areas: [computing]
tags: [operating-systems, processes]
requires: []
unlocks: ["[[context-switch]]"]
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Estados de un proceso

## Modelo de 5 estados

Un proceso transita por los siguientes estados durante su vida:

- **New** — recién creado, aún no admitido al sistema.
- **Ready** — listo para ejecutar, esperando CPU.
- **Running** — ejecutándose en una CPU.
- **Blocked / Waiting** — esperando un evento (I/O, signal, semáforo, mailbox).
- **Terminated / Exit** — finalizó (terminó o fue cancelado).

## Transiciones clave

- `New → Ready`: admisión por el planificador de largo plazo.
- `Ready → Running`: planificador de corto plazo (dispatch).
- `Running → Ready`: preempción (quantum expirado, proceso de mayor prioridad apareció).
- `Running → Blocked`: el proceso pidió I/O o sincronización y se suspendió.
- `Blocked → Ready`: el evento esperado ocurrió.
- `Running → Terminated`: el proceso terminó (`exit()` o equivalente).

## En cada transición

El SO actualiza el campo `estado` del [[process-control-block]] del proceso. En transiciones desde y hacia `Running` también ocurre un [[context-switch]].

## Conexiones

- Estado vive en: [[process-control-block]] (campo `estado`).
- Cambios de estado disparan: [[context-switch]] (cuando hay cambio de proceso en CPU).
- Aparece en: Sistemas Operativos, Tema 2 (Procesos y planificación).
