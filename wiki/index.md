---
type: index
updated: 2026-06-02
---

# Wiki — catálogo

Punto de entrada del wiki. Lista todas las páginas activas agrupadas por tipo. Cada modo (`/ingest`, `/query`, `/practice`, `/lint`) usa este archivo para localizar candidatos antes de leer páginas individuales.

> Para Dataview (Obsidian): los bloques de abajo se renderizan automáticamente. Sin Dataview, la lista manual de fallback se mantiene actualizada por los modos `/ingest` y `/query`.

---

## Conceptos

```dataview
TABLE areas, file.mtime AS "Actualizado"
FROM "wiki/concepts"
SORT file.name ASC
```

### Fallback manual
- [[critical-point]]
- [[curve-parametrization]]
- [[jacobian]]
- [[arc-length]]
- [[line-integral]]
- [[gradient-field]]
- [[parametric-surface]]
- [[surface-integral]]
- [[curl]]
- [[divergence]]
- [[irrotational-field]]
- [[solenoidal-field]]
- [[process-control-block]]
- [[process-states]]
- [[context-switch]]
- [[thread]]
- [[regular-expression]]
- [[finite-automaton]]
- [[singular-value-decomposition]]
- [[singular-values]]
- [[unitary-matrix]]
- [[low-rank-approximation]]
- [[frobenius-norm]]
- [[spectral-norm]]
- [[four-fundamental-subspaces]]
- [[pseudo-inverse]]
- [[condition-number]]
- [[principal-component-analysis]]
- [[covariance-matrix]]
- [[randomized-svd]]
- [[tensor-decomposition]]

---

## Teoremas

```dataview
TABLE areas, statement_form
FROM "wiki/theorems"
SORT file.name ASC
```

### Fallback manual
- [[implicit-function-theorem]]
- [[greens-theorem]]
- [[stokes-theorem]]
- [[gauss-theorem]]
- [[arden-lemma]]
- [[eckart-young-theorem]]

---

## Métodos

```dataview
TABLE areas, when_to_use
FROM "wiki/methods"
SORT file.name ASC
```

### Fallback manual
- [[hessian-criterion]]
- [[kleene-analysis]]
- [[normal-vector-parametric-surface]]
- [[method-of-snapshots]]
- [[optimal-hard-threshold]]
- [[least-squares-regression]]

---

## Ejemplos

```dataview
TABLE difficulty, illustrates, areas
FROM "wiki/examples"
SORT file.mtime DESC
```

### Fallback manual
- [[cycloid-parametrization]]
- [[circle-parametrization]]
- [[line-segment-parametrization]]
- [[helix-parametrization]]

---

## Comparaciones

```dataview
TABLE compares, areas
FROM "wiki/comparisons"
SORT file.mtime DESC
```

### Fallback manual
(ninguna todavía)

---

## Fuentes

```dataview
TABLE source_kind, path, areas
FROM "wiki/sources"
SORT file.mtime DESC
```

### Fallback manual
- [[gonzalez-cvec-2023]]
- [[brunton-kutz-ch1]]

---

## Áreas (MOCs)

- [[areas/math]]
- [[areas/signals]]
- [[areas/computing]]
- [[areas/engineering-physics]]
- [[areas/ml]]
