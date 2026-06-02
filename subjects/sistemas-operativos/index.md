---
updated: 2026-03-18
---

# Índice: Sistemas Operativos

## Temario del curso

### PRIMERA PARTE

#### Tema 1 — Introducción y estructura (Semanas 1–2) · Prácticos 1 y 2
- Introducción a los sistemas de computación
- Concepto y objetivos de un SO
- Estructura de los sistemas operativos
- Llamadas al sistema (system calls)

#### Tema 2 — Procesos y planificación (Semana 3) · Práctico 2
- Concepto de proceso y estados
- Creación y finalización de procesos
- Planificación de CPU
- Algoritmos de planificación

#### Tema 3 — Concurrencia y sincronización (Semanas 4–8) · Prácticos 3, 4 y 5
- Introducción a la concurrencia
- Sección crítica
- Sincronización
- Semáforos
- Monitores
- Mailboxes
- Deadlock

### SEGUNDA PARTE

#### Tema 4 — Sistemas de archivos (Semanas 10–11) · Práctico 6
- Concepto de archivo
- Estructura de directorios
- Implementación de sistemas de archivos
- Métodos de asignación

#### Tema 5 — Almacenamiento y E/S (Semanas 11–12) · Práctico 7
- Dispositivos de almacenamiento
- Planificación de disco
- RAID
- Entrada/Salida

#### Tema 6 — Memoria (Semanas 12–13) · Prácticos 8 y 9
- Administración de memoria
- Paginación
- Segmentación
- Memoria virtual

#### Tema 7 — Protección y seguridad (Semana 14) · Práctico 10
- Concepto de protección
- Mecanismos de seguridad
- Control de acceso

#### Tema 8 — Virtualización y tendencias (Semana 15)
- Concepto de virtualización
- Máquinas virtuales
- Tendencias actuales

## Notación del curso
(completar según material del curso)

## Conceptos

### Entiendo
- PCB: estructura, campos, y por qué se guardan los registros de CPU
- Estados de un proceso y transiciones
- Context switch entre procesos (secuencia completa)
- Qué comparte un thread con los demás threads del mismo proceso (code, data, files) vs. qué es privado (registros, stack)

### Tengo dudas
- Context switch entre threads: la secuencia formal no fue escrita, solo conceptualizada

## Bloom actual
- Procesos y PCB: Comprensión/Aplicación (Bloom 2–3)
- Threads: Comprensión (Bloom 2); falta práctica de aplicación en ejercicios de planificación

## Sesiones con Claude
| Fecha | Ejercicios / temas trabajados | Resultado |
|---|---|---|
| (se llena automático al cierre de cada sesión) | | |
| 2026-03-18 | Ej 1(a)(b)(c): estados de proceso, PCB, registros en PCB. Ej 2(a): context switch procesos y threads (conceptual) | Correcto con una iteración en 1c; 2a procesos completo, threads conceptualizado sin formalizar |

## Conceptos wiki

```dataview
TABLE bloom, areas, type
FROM "wiki/concepts" OR "wiki/theorems" OR "wiki/methods" OR "wiki/examples"
WHERE contains(seen_in_subjects, regexreplace(this.file.folder, ".*/", ""))
SORT bloom DESC, file.name ASC
```

### Fallback manual
- [[process-control-block]] (bloom 3)
- [[process-states]] (bloom 3)
- [[context-switch]] (bloom 2)
- [[thread]] (bloom 2)

> La verdad ejecutable del Bloom vive en el frontmatter de cada página wiki — la sección "Bloom actual" de arriba es referencia humana.
