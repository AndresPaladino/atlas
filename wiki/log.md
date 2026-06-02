---
type: log
updated: 2026-06-02
---

# Log del wiki

Append-only. Una entrada por operación que modificó el wiki (`/ingest`, `/query` con file-back, `/practice` al cierre, `/lint` con fixes). Formato: `## [YYYY-MM-DD] <op> | <descripción corta>`.

El log es **concept-bound**: registra qué pasó al grafo de conocimiento. El registro **course-bound** (qué pasó en cada sesión por materia) vive en `subjects/[materia]/index.md`. Ambos se actualizan en paralelo al cerrar una sesión `/practice`.

---

## [2026-06-02] bootstrap | Wiki inicial

- Creación de la estructura `wiki/` (concepts, theorems, methods, examples, comparisons, sources, areas).
- Migración inicial de Bloom desde `subjects/*/index.md`:
  - Cálc Vect: [[hessian-criterion]] (b2), [[critical-point]] (b2), [[implicit-function-theorem]] (b2), [[jacobian]] (b1), [[curve-parametrization]] (b2), [[cycloid-parametrization]] (b2)
  - Sistemas Operativos: [[process-control-block]] (b3), [[process-states]] (b3), [[context-switch]] (b2), [[thread]] (b2)
  - Teoría de Lenguajes: [[kleene-analysis]] (b3), [[arden-lemma]] (b3), [[regular-expression]] (b3), [[finite-automaton]] (b2)
- 13 páginas wiki creadas con frontmatter completo y contenido mínimo viable.
- Física 1: sin migración (Bloom default todavía).
