---
type: source
title: "Data-Driven Science and Engineering — Chapter 1: SVD"
aliases: ["Brunton & Kutz Ch. 1", "brunton-kutz-svd"]
source_kind: book
path: "raw/Data-Driven Science and Engineering_p29-p85.pdf"
pages: "29-85"
areas: [data-science, linear-algebra]
tags: [linear-algebra/matrix-decomposition]
covers_concepts:
  - "[[singular-value-decomposition]]"
  - "[[singular-values]]"
  - "[[unitary-matrix]]"
  - "[[low-rank-approximation]]"
  - "[[frobenius-norm]]"
  - "[[spectral-norm]]"
  - "[[four-fundamental-subspaces]]"
  - "[[pseudo-inverse]]"
  - "[[condition-number]]"
  - "[[principal-component-analysis]]"
  - "[[covariance-matrix]]"
  - "[[randomized-svd]]"
  - "[[tensor-decomposition]]"
covers_theorems:
  - "[[eckart-young-theorem]]"
covers_methods:
  - "[[method-of-snapshots]]"
  - "[[optimal-hard-threshold]]"
  - "[[least-squares-regression]]"
created: 2026-06-02
updated: 2026-06-02
---

## Mapa de coverage

| Sección | Páginas (libro) | Concepto wiki |
|---|---|---|
| §1.1 Definition of the SVD | 31–34 | [[singular-value-decomposition]], [[singular-values]], [[unitary-matrix]] |
| §1.2 Matrix Approximation | 35–40 | [[low-rank-approximation]], [[eckart-young-theorem]], [[frobenius-norm]], [[spectral-norm]] |
| §1.3 Mathematical Properties | 41–45 | [[method-of-snapshots]], [[four-fundamental-subspaces]], [[unitary-matrix]] |
| §1.4 Pseudo-Inverse, Least-Squares | 46–53 | [[pseudo-inverse]], [[least-squares-regression]], [[condition-number]], [[four-fundamental-subspaces]] |
| §1.5 Principal Component Analysis | 54–61 | [[principal-component-analysis]], [[covariance-matrix]] |
| §1.6 Eigenfaces Example | 61–67 | [[principal-component-analysis]] |
| §1.7 Truncation and Alignment | 68–75 | [[optimal-hard-threshold]], [[low-rank-approximation]] |
| §1.8 Randomized SVD | 76–81 | [[randomized-svd]] |
| §1.9 Tensor Decompositions | 82–85 | [[tensor-decomposition]] |

## Notas

- Notación: columnas de X son "snapshots" (mediciones en distintos instantes). Convención $n \gg m$ (tall-skinny).
- Python: `np.linalg.svd` retorna $V^T$ (no $V$), a diferencia de MATLAB.
- PCA en §1.5 usa convención estadística donde X tiene mediciones por filas (distinto al resto del capítulo).
- Copyright © 2021 Brunton & Kutz, Cambridge University Press.
