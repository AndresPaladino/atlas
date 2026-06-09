---
type: concept
title: "Singular Values"
aliases: ["valores singulares", "σ_k", "singular value spectrum"]
areas: [linear-algebra, data-science]
tags: [linear-algebra/matrix-decomposition]
requires: []
unlocks: ["[[singular-value-decomposition]]", "[[condition-number]]", "[[spectral-norm]]", "[[low-rank-approximation]]"]
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Los valores singulares de una matriz $\mathbf{X} \in \mathbb{C}^{n \times m}$ son las entradas diagonales $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_m \geq 0$ de la matriz $\boldsymbol{\Sigma}$ en la [[singular-value-decomposition|SVD]] $\mathbf{X} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^*$ [[brunton-kutz-ch1]] §1.1 p. 31.

Equivalentemente, $\sigma_k = \sqrt{\lambda_k(\mathbf{X}^*\mathbf{X})}$, donde $\lambda_k$ son los eigenvalores de $\mathbf{X}^*\mathbf{X}$ ordenados de mayor a menor.

## Intuición

Los valores singulares miden cuánta "energía" o varianza captura cada modo de la descomposición. Si los $\sigma_k$ decrecen rápidamente, la matriz tiene estructura de bajo rango: unos pocos modos dominan y el resto es ruido o información redundante. Sistemas físicos complejos (flujos, imágenes, series temporales) suelen exhibir este patrón [[brunton-kutz-ch1]] §1.1 p. 30.

## Propiedades

- El rango de $\mathbf{X}$ es igual al número de valores singulares no nulos.
- Si $\mathbf{X} = \mathbf{X}^*$ (Hermitiana), los valores singulares son el valor absoluto de los eigenvalores.
- Los valores singulares son invariantes a transformaciones unitarias por izquierda o derecha.

## Conexiones

- Habilita: [[singular-value-decomposition]], [[condition-number]], [[spectral-norm]], [[low-rank-approximation]], [[optimal-hard-threshold]]

## Fuentes

- [[brunton-kutz-ch1]] §1.1 p. 31, §1.3 pp. 41–42
