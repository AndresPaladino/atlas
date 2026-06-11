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
TABLE tags
FROM "wiki/concepts"
WHERE contains(areas, "computing")
SORT file.name ASC
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
TABLE statement_form
FROM "wiki/theorems"
WHERE contains(areas, "computing")
SORT file.name ASC
```

### Fallback manual
- [[arden-lemma]]

## Métodos

```dataview
TABLE when_to_use
FROM "wiki/methods"
WHERE contains(areas, "computing")
SORT file.name ASC
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
