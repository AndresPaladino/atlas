---
type: log
updated: 2026-06-02
---

# Log del wiki

Append-only. Una entrada por operación que modificó el wiki (`/ingest`, `/query` con file-back, `/practice` al cierre, `/lint` con fixes). Formato: `## [YYYY-MM-DD] <op> | <descripción corta>`.

El log es **concept-bound**: registra qué pasó al grafo de conocimiento. El registro **course-bound** (qué pasó en cada sesión por materia) vive en `subjects/[materia]/index.md`. Ambos se actualizan en paralelo al cerrar una sesión `/practice`.

---

## [2026-06-04] query | Parametrización de curvas — ejemplos básicos

- Páginas creadas (3 ejemplos): [[circle-parametrization]], [[line-segment-parametrization]], [[helix-parametrization]]
- Ilustran: [[curve-parametrization]]

---

## [2026-06-02] ingest | Data-Driven Science and Engineering — Ch. 1 (Brunton & Kutz)

- Fuente: [[brunton-kutz-ch1]] (`raw/Data-Driven Science and Engineering_p29-p85.pdf`)
- Páginas wiki creadas (13 conceptos):
  [[singular-value-decomposition]], [[singular-values]], [[unitary-matrix]], [[low-rank-approximation]], [[frobenius-norm]], [[spectral-norm]], [[four-fundamental-subspaces]], [[pseudo-inverse]], [[condition-number]], [[principal-component-analysis]], [[covariance-matrix]], [[randomized-svd]], [[tensor-decomposition]]
- Páginas wiki creadas (1 teorema):
  [[eckart-young-theorem]]
- Páginas wiki creadas (3 métodos):
  [[method-of-snapshots]], [[optimal-hard-threshold]], [[least-squares-regression]]
- Aristas nuevas destacadas:
  [[singular-value-decomposition]] requires [[unitary-matrix]], [[singular-values]];
  [[singular-value-decomposition]] unlocks [[low-rank-approximation]], [[pseudo-inverse]], [[principal-component-analysis]], [[four-fundamental-subspaces]];
  [[eckart-young-theorem]] requires [[low-rank-approximation]], [[frobenius-norm]], [[spectral-norm]];
  [[pseudo-inverse]] requires [[four-fundamental-subspaces]];
  [[least-squares-regression]] requires [[pseudo-inverse]];
  [[principal-component-analysis]] requires [[covariance-matrix]];
  [[optimal-hard-threshold]] requires [[eckart-young-theorem]]

---

## [2026-06-02] query | versor normal a superficie paramétrica

- Página creada: [[normal-vector-parametric-surface]]
- Fuentes citadas: [[gonzalez-cvec-2023]]

---

## [2026-06-02] ingest | NotasCursoCVec2023.pdf

- Fuente: [[gonzalez-cvec-2023]] (`raw/NotasCursoCVec2023.pdf`)
- Scope: Capítulo 2 (§2.1–§2.9, pp. 37–113)
- Páginas wiki creadas:
  - [[arc-length]], [[line-integral]], [[gradient-field]], [[parametric-surface]], [[surface-integral]]
  - [[curl]], [[divergence]], [[irrotational-field]], [[solenoidal-field]]
  - [[greens-theorem]], [[stokes-theorem]], [[gauss-theorem]]
- Páginas wiki actualizadas: [[curve-parametrization]] (sources +1, unlocks actualizado)
- Aristas nuevas: [[arc-length]] requires [[curve-parametrization]]; [[line-integral]] requires [[arc-length]]; [[gradient-field]] requires [[line-integral]]; [[greens-theorem]] requires [[line-integral]], [[gradient-field]]; [[parametric-surface]] requires [[curve-parametrization]], [[jacobian]]; [[surface-integral]] requires [[parametric-surface]]; [[stokes-theorem]] requires [[surface-integral]], [[curl]], [[greens-theorem]]; [[gauss-theorem]] requires [[surface-integral]], [[divergence]]; [[curl]] unlocks [[irrotational-field]], [[stokes-theorem]]; [[divergence]] unlocks [[solenoidal-field]], [[gauss-theorem]]

---

## [2026-06-02] bootstrap | Wiki inicial

- Creación de la estructura `wiki/` (concepts, theorems, methods, examples, comparisons, sources, areas).
- Migración inicial de Bloom desde `subjects/*/index.md`:
  - Cálc Vect: [[hessian-criterion]] (b2), [[critical-point]] (b2), [[implicit-function-theorem]] (b2), [[jacobian]] (b1), [[curve-parametrization]] (b2), [[cycloid-parametrization]] (b2)
  - Sistemas Operativos: [[process-control-block]] (b3), [[process-states]] (b3), [[context-switch]] (b2), [[thread]] (b2)
  - Teoría de Lenguajes: [[kleene-analysis]] (b3), [[arden-lemma]] (b3), [[regular-expression]] (b3), [[finite-automaton]] (b2)
- 13 páginas wiki creadas con frontmatter completo y contenido mínimo viable.
- Física 1: sin migración (Bloom default todavía).
