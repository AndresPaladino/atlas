---
type: concept
title: "Low-Rank Approximation"
aliases: ["aproximación de bajo rango", "truncated SVD", "SVD truncada", "rank-r approximation"]
areas: [linear-algebra, data-science]
tags: [linear-algebra/matrix-decomposition, data-science/dimensionality-reduction]
requires: ["[[singular-value-decomposition]]", "[[singular-values]]"]
unlocks: ["[[eckart-young-theorem]]", "[[randomized-svd]]", "[[principal-component-analysis]]"]
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Una **aproximación de rango $r$** a una matriz $\mathbf{X} \in \mathbb{C}^{n \times m}$ es la suma de los primeros $r$ términos de la expansión diádica de la [[singular-value-decomposition|SVD]]:

$$\tilde{\mathbf{X}} = \sum_{k=1}^{r} \sigma_k \mathbf{u}_k \mathbf{v}_k^* = \tilde{\mathbf{U}}\tilde{\boldsymbol{\Sigma}}\tilde{\mathbf{V}}^*,$$

donde $\tilde{\mathbf{U}}$ y $\tilde{\mathbf{V}}$ contienen las primeras $r$ columnas de $\mathbf{U}$ y $\mathbf{V}$, y $\tilde{\boldsymbol{\Sigma}}$ es el sub-bloque $r \times r$ de $\boldsymbol{\Sigma}$ [[brunton-kutz-ch1]] §1.2 p. 35.

## Intuición

Si los [[singular-values|valores singulares]] $\sigma_k$ decrecen rápidamente, los primeros $r$ modos capturan la mayor parte de la "energía" de $\mathbf{X}$. Mantener solo $r$ modos comprime la representación: en vez de $n \times m$ números, basta almacenar $r(n + m + 1)$ números (las columnas de $\tilde{\mathbf{U}}$, $\tilde{\mathbf{V}}$, y los $r$ valores singulares). Ejemplo: una imagen de $2000 \times 1500$ con $r=100$ requiere solo el $11.67\%$ del almacenamiento original [[brunton-kutz-ch1]] §1.2 p. 38.

## Error de la aproximación

El error en norma Frobenius es exactamente:

$$\|\mathbf{X} - \tilde{\mathbf{X}}\|_F^2 = \sum_{k=r+1}^{m} \sigma_k^2.$$

En norma espectral: $\|\mathbf{X} - \tilde{\mathbf{X}}\|_2 = \sigma_{r+1}$.

El [[eckart-young-theorem|Teorema de Eckart-Young]] garantiza que no existe ninguna otra matriz de rango $r$ con menor error en estas normas.

## Cómo elegir r

- **Energía acumulada**: mantener $r$ tal que $\sum_{k=1}^r \sigma_k / \sum_{k=1}^m \sigma_k \geq \theta$ (típicamente $\theta = 0.90$ o $0.99$).
- **"Codo" (elbow)**: buscar la transición en la distribución de valores singulares entre modos dominantes y ruido.
- **[[optimal-hard-threshold|Umbral óptimo de Gavish-Donoho]]**: si el ruido es Gaussiano con magnitud conocida o estimable.

## Conexiones

- Requiere: [[singular-value-decomposition]], [[singular-values]]
- Habilita: [[eckart-young-theorem]], [[randomized-svd]], [[principal-component-analysis]]
- Relacionado: [[optimal-hard-threshold]], [[frobenius-norm]], [[spectral-norm]]

## Fuentes

- [[brunton-kutz-ch1]] §1.2 pp. 35–40, §1.7 pp. 68–75
