---
type: area
title: "Matemática"
tag_prefix: "math"
updated: 2026-06-02
---

# Math — MOC

Área que agrupa cálculo, álgebra, análisis, geometría, lógica matemática. Incluye temas de matemática base aplicables a varias materias (cálculo vectorial, física, ML, signals).

## Conceptos

```dataview
TABLE bloom, tags
FROM "wiki/concepts"
WHERE contains(areas, "math")
SORT bloom DESC, file.name ASC
```

### Fallback manual
- [[critical-point]]
- [[curve-parametrization]]
- [[jacobian]]

## Teoremas

```dataview
TABLE bloom, statement_form
FROM "wiki/theorems"
WHERE contains(areas, "math")
SORT bloom DESC
```

### Fallback manual
- [[implicit-function-theorem]]

## Métodos

```dataview
TABLE bloom, when_to_use
FROM "wiki/methods"
WHERE contains(areas, "math")
SORT bloom DESC
```

### Fallback manual
- [[hessian-criterion]]

## Ejemplos

```dataview
TABLE difficulty, illustrates
FROM "wiki/examples"
WHERE contains(areas, "math")
SORT file.mtime DESC
```

### Fallback manual
- [[cycloid-parametrization]]

## Comparaciones

```dataview
TABLE compares
FROM "wiki/comparisons"
WHERE contains(areas, "math")
```

### Fallback manual
(ninguna)
