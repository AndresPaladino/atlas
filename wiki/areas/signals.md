---
type: area
title: "Señales y sistemas"
tag_prefix: "signals"
updated: 2026-06-02
---

# Signals — MOC

Área que agrupa procesamiento de señales, sistemas LTI, transformadas (Fourier, Laplace, z), filtros, muestreo. También: teoría de la información, comunicaciones digitales.

## Conceptos

```dataview
TABLE bloom, tags
FROM "wiki/concepts"
WHERE contains(areas, "signals")
SORT bloom DESC, file.name ASC
```

### Fallback manual
(ninguno todavía)

## Teoremas

```dataview
TABLE bloom, statement_form
FROM "wiki/theorems"
WHERE contains(areas, "signals")
SORT bloom DESC
```

### Fallback manual
(ninguno todavía)

## Métodos

```dataview
TABLE bloom, when_to_use
FROM "wiki/methods"
WHERE contains(areas, "signals")
SORT bloom DESC
```

### Fallback manual
(ninguno todavía)

## Ejemplos

```dataview
TABLE difficulty, illustrates
FROM "wiki/examples"
WHERE contains(areas, "signals")
SORT file.mtime DESC
```

### Fallback manual
(ninguno todavía)
