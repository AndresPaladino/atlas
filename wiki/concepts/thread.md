---
type: concept
title: "Thread"
aliases: ["hilo", "thread", "hilo de ejecución"]
areas: [computing]
tags: [operating-systems, concurrency]
requires: []
unlocks: []
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Thread

## Definición

Un **thread** (hilo) es una unidad de ejecución dentro de un proceso. Un proceso tiene al menos un thread; puede tener múltiples threads concurrentes que comparten recursos del proceso.

## Qué comparten los threads de un proceso

- **Code segment** — código ejecutable.
- **Data segment** — variables globales y estáticas.
- **Heap** — memoria asignada dinámicamente.
- **File descriptors** y otros recursos del SO asignados al proceso.
- **Espacio de direcciones** completo.

## Qué es privado de cada thread

- **Registros de CPU** (program counter, registros generales).
- **Stack** — variables locales, parámetros de funciones, return addresses.
- **Thread ID**.
- **Información de planificación específica del thread** (prioridad, política, si el sistema lo soporta a nivel thread).

## Modelos de threads

- **User-level threads** (ULT): gestionados por una librería en espacio de usuario; el kernel ve un solo thread por proceso.
- **Kernel-level threads** (KLT): el kernel conoce y planifica cada thread.
- **Modelos híbridos** (M:N): N threads de usuario sobre M threads de kernel.

## Implicaciones para [[context-switch]]

Entre threads del mismo proceso, el switch es más barato: no cambia espacio de direcciones, no flush total de TLB. Esto motiva el uso de threads donde alcanzaría con procesos pero el costo sería prohibitivo (ej: servidor web atendiendo muchas conexiones).

## Conexiones

- Habilita: [[context-switch]] (variante thread)
- Relacionado con: concurrencia, sincronización (Tema 3 de SO).
- Aparece en: Sistemas Operativos, Tema 2 (Procesos) y Tema 3 (Concurrencia).
