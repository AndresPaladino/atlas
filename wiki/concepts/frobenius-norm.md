---
type: concept
title: "Frobenius Norm"
aliases: ["norma de Frobenius", "‖X‖_F", "norma Frobenius"]
areas: [linear-algebra]
tags: [linear-algebra/norms]
requires: []
unlocks: ["[[eckart-young-theorem]]", "[[low-rank-approximation]]"]
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Definición

La **norma de Frobenius** de una matriz $\mathbf{X} \in \mathbb{C}^{n \times m}$ es

$$\|\mathbf{X}\|_F = \sqrt{\sum_{i=1}^{n} \sum_{j=1}^{m} |X_{ij}|^2},$$

equivalente a la norma $\ell_2$ del vector obtenido por vectorización de $\mathbf{X}$ [[brunton-kutz-ch1]] §1.2 p. 36.

## Intuición

La norma Frobenius mide el "tamaño total" de una matriz como si fuera un vector largo. Para matrices de datos donde las columnas son campos de velocidad (e.g., simulaciones de fluidos), el error al cuadrado $\|\mathbf{X} - \tilde{\mathbf{X}}\|_F^2$ tiene la interpretación de la **energía cinética faltante** en la aproximación [[brunton-kutz-ch1]] §1.2 p. 37. Más generalmente, para datos centrados, representa la varianza perdida.

## Relación con valores singulares

$$\|\mathbf{X}\|_F^2 = \sum_{k=1}^{m} \sigma_k^2 = \mathrm{tr}(\mathbf{X}^*\mathbf{X}).$$

Esto permite calcular el error de la [[low-rank-approximation|SVD truncada]] directamente de los valores singulares descartados.

## Conexiones

- Habilita: [[eckart-young-theorem]], [[low-rank-approximation]]
- Relacionado: [[spectral-norm]], [[singular-values]]

## Fuentes

- [[brunton-kutz-ch1]] §1.2 p. 36
