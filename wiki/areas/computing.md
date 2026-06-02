---
type: area
title: "Computación"
tag_prefix: "computing"
updated: 2026-06-02
---

# Computing — MOC

Área que agrupa sistemas operativos, teoría de la computación, lenguajes formales, autómatas, complejidad, redes, arquitectura. Materias activas que aportan: Sistemas Operativos, Teoría de Lenguajes.

## Conceptos

```dataview
TABLE bloom, tags
FROM "wiki/concepts"
WHERE contains(areas, "computing")
SORT bloom DESC, file.name ASC
```

### Fallback manual
- [[process-control-block]]
- [[process-states]]
- [[context-switch]]
- [[thread]]
- [[regular-expression]]
- [[finite-automaton]]

## Teoremas

```dataview
TABLE bloom, statement_form
FROM "wiki/theorems"
WHERE contains(areas, "computing")
SORT bloom DESC
```

### Fallback manual
- [[arden-lemma]]

## Métodos

```dataview
TABLE bloom, when_to_use
FROM "wiki/methods"
WHERE contains(areas, "computing")
SORT bloom DESC
```

### Fallback manual
- [[kleene-analysis]]

## Ejemplos

```dataview
TABLE difficulty, illustrates
FROM "wiki/examples"
WHERE contains(areas, "computing")
SORT file.mtime DESC
```

### Fallback manual
(ninguno todavía)
