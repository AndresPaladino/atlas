---
type: area
title: "Machine Learning"
tag_prefix: "ml"
updated: 2026-06-02
---

# ML — MOC

Área que agrupa machine learning clásico (regresión, clasificación, clustering), deep learning, optimización, probabilidad y estadística aplicada a ML. Sin materia activa en la carrera todavía — esta área se puebla con interés propio.

## Conceptos

```dataview
TABLE bloom, tags
FROM "wiki/concepts"
WHERE contains(areas, "ml")
SORT bloom DESC, file.name ASC
```

### Fallback manual
(ninguno todavía)

## Teoremas

```dataview
TABLE bloom, statement_form
FROM "wiki/theorems"
WHERE contains(areas, "ml")
SORT bloom DESC
```

### Fallback manual
(ninguno todavía)

## Métodos

```dataview
TABLE bloom, when_to_use
FROM "wiki/methods"
WHERE contains(areas, "ml")
SORT bloom DESC
```

### Fallback manual
(ninguno todavía)
