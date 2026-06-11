---
type: concept
title: "Process Control Block (PCB)"
aliases: ["PCB", "bloque de control de proceso", "task struct"]
areas: [computing]
tags: [operating-systems, processes]
requires: []
unlocks: ["[[context-switch]]"]
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Process Control Block (PCB)

## Definición

El **PCB** es la estructura de datos que el sistema operativo mantiene **por cada proceso** activo. Contiene toda la información que el SO necesita para administrar y, sobre todo, suspender y reanudar el proceso.

## Campos típicos

- **Identificador de proceso** (PID) y, si aplica, PPID (padre).
- **Estado** del proceso (ver [[process-states]]).
- **Program counter** — siguiente instrucción a ejecutar.
- **Registros de CPU** — copia de los registros generales y de propósito especial.
- **Información de planificación** — prioridad, quantum restante, política.
- **Información de memoria** — tablas de páginas, base/límite, segmentos.
- **Información de E/S** — dispositivos asignados, descriptores de archivo abiertos.
- **Contabilidad** — tiempo de CPU consumido, recursos.

## Por qué se guardan los registros

Cuando el SO decide quitar al proceso de la CPU (preempción, llamada al sistema, espera), los registros físicos del CPU pasan a contener el contexto de otro proceso. Si no se hubieran guardado en el PCB del proceso saliente, al reanudarlo no se podría restaurar su ejecución exacta — el proceso vería estado corrupto.

## Conexiones

- Habilita: [[context-switch]] (el PCB es el destino de la operación save/restore).
- Estados que se mantienen acá: [[process-states]].
- Aparece en: Sistemas Operativos, Tema 2 (Procesos y planificación).
