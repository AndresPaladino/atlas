---
type: concept
title: "Context switch"
aliases: ["cambio de contexto", "switch de contexto"]
areas: [computing]
tags: [operating-systems, processes, scheduling]
requires: ["[[process-control-block]]", "[[process-states]]"]
unlocks: []
bloom: 2
sources: []
seen_in_subjects: [sistemas-operativos]
created: 2026-06-02
updated: 2026-06-02
---

# Context switch

## Definición

**Context switch** es la operación mediante la cual el SO retira un proceso (o thread) de la CPU y pone otro en su lugar, preservando la posibilidad de reanudar el saliente en el futuro exactamente donde quedó.

## Secuencia (entre procesos)

Dado que el proceso $P_1$ está en `Running` y el SO decide darle la CPU a $P_2`:

1. **Trap / interrupción**: hardware o software fuerza la entrada al SO.
2. **Save state de $P_1$**: copiar registros de CPU (program counter, registros generales, flags) al [[process-control-block]] de $P_1$.
3. **Cambiar estado de $P_1$**: típicamente a `Ready` o `Blocked`.
4. **Planificador**: seleccionar $P_2$ de la cola de `Ready`.
5. **Restore state de $P_2$**: copiar desde el PCB de $P_2$ a los registros físicos del CPU.
6. **Cambiar estado de $P_2$** a `Running`.
7. **Cambio de espacio de direcciones**: actualizar el MMU (tablas de páginas, registro base) para que $P_2$ vea su memoria. Esto incluye flush parcial de la TLB.
8. **Retorno**: el program counter restaurado apunta a la siguiente instrucción de $P_2$; el CPU sigue desde allí.

## Diferencia entre proceso y thread

- **Entre threads del mismo proceso**: el espacio de direcciones se comparte → paso 7 se omite. Solo cambian registros, stack pointer, y program counter. Mucho más barato.
- **Entre threads de procesos distintos**: equivalente a context switch entre procesos.

Lo que comparten threads del mismo proceso (no requiere switch): code, data, heap, file descriptors.
Lo que es privado por thread (sí requiere switch): registros, stack, program counter.

## Costo

El switch tiene costo medible: cycles para save/restore, flush de TLB (en switches entre procesos), pérdida de localidad de caches. Sistemas modernos optimizan threads precisamente para evitar el costo del cambio de espacio de direcciones.

## Conexiones

- Requiere: [[process-control-block]], [[process-states]]
- Relacionado con: [[thread]]
- Aparece en: Sistemas Operativos, Tema 2 (Procesos) y Tema 3 (Concurrencia).
