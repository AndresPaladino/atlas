---
type: concept
title: "Spectral Norm (Matrix 2-Norm)"
aliases: ["norma espectral", "matrix 2-norm", "2-norma matricial", "‖X‖_2"]
areas: [linear-algebra]
tags: [linear-algebra/norms]
requires: ["[[singular-values]]"]
unlocks: ["[[eckart-young-theorem]]", "[[condition-number]]"]
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Definición

La **norma espectral** (o 2-norma matricial) de $\mathbf{X} \in \mathbb{C}^{n \times m}$ es la norma inducida por la norma vectorial $\ell_2$:

$$\|\mathbf{X}\|_2 = \max_{\mathbf{v} \neq 0} \frac{\|\mathbf{X}\mathbf{v}\|_2}{\|\mathbf{v}\|_2} = \sigma_1(\mathbf{X}),$$

es decir, el mayor [[singular-values|valor singular]] de $\mathbf{X}$ [[brunton-kutz-ch1]] §1.2 p. 37.

## Intuición

La norma espectral mide el **máximo factor de amplificación** que la transformación $\mathbf{X}$ puede aplicar a cualquier vector unitario. Es la medida natural del "tamaño" de $\mathbf{X}$ como operador lineal.

## Relación con la SVD truncada

El error de la [[low-rank-approximation|aproximación de rango $r$]] en norma espectral es exactamente el siguiente valor singular:

$$\|\mathbf{X} - \tilde{\mathbf{X}}\|_2 = \sigma_{r+1}.$$

## Conexiones

- Requiere: [[singular-values]]
- Habilita: [[eckart-young-theorem]], [[condition-number]]
- Relacionado: [[frobenius-norm]]

## Fuentes

- [[brunton-kutz-ch1]] §1.2 p. 37
