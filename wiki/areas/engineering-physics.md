---
type: area
title: "Física aplicada / ingeniería"
tag_prefix: "engineering-physics"
updated: 2026-06-02
---

# Engineering-Physics — MOC

Área que agrupa mecánica clásica, electromagnetismo, oscilaciones, ondas, termodinámica, óptica, mecánica de cuerpo rígido. Materias activas que aportan: Física 1.

## Conceptos

```dataview
TABLE bloom, tags
FROM "wiki/concepts"
WHERE contains(areas, "engineering-physics")
SORT bloom DESC, file.name ASC
```

### Fallback manual
(ninguno todavía — Física 1 pendiente de ingest)

## Teoremas

```dataview
TABLE bloom, statement_form
FROM "wiki/theorems"
WHERE contains(areas, "engineering-physics")
SORT bloom DESC
```

### Fallback manual
(ninguno todavía)

## Métodos

```dataview
TABLE bloom, when_to_use
FROM "wiki/methods"
WHERE contains(areas, "engineering-physics")
SORT bloom DESC
```

### Fallback manual
(ninguno todavía)

## Ejemplos

```dataview
TABLE difficulty, illustrates
FROM "wiki/examples"
WHERE contains(areas, "engineering-physics")
SORT file.mtime DESC
```

### Fallback manual
(ninguno todavía)
