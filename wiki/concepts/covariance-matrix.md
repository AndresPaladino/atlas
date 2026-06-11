---
type: concept
title: "Covariance Matrix"
aliases: ["matriz de covarianza", "C", "covariance matrix"]
areas: [linear-algebra, statistics]
tags: [statistics/multivariate, linear-algebra/matrix-properties]
requires: []
unlocks: ["[[principal-component-analysis]]"]
sources: ["[[brunton-kutz-ch1]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Dada una matriz de datos $\mathbf{B} \in \mathbb{R}^{n \times m}$ (con media substraída por filas), la **matriz de covarianza** es

$$\mathbf{C} = \frac{1}{n-1}\mathbf{B}^*\mathbf{B} \in \mathbb{R}^{m \times m},$$

donde la normalización por $n-1$ (corrección de Bessel) compensa el sesgo de la varianza muestral [[brunton-kutz-ch1]] §1.5 p. 54.

## Intuición

La entrada $C_{ij}$ cuantifica la **correlación** entre las características $i$ y $j$ a través de todos los experimentos. Una $\mathbf{C}$ diagonal implica características linealmente no correlacionadas. La [[principal-component-analysis|PCA]] busca exactamente una base (los eigenvectores de $\mathbf{C}$) en la que $\mathbf{C}$ sea diagonal.

## Propiedades

- $\mathbf{C}$ es simétrica y **semidefinida positiva** (eigenvalores $\geq 0$).
- Sus eigenvectores son los vectores singulares derechos de $\mathbf{B}$ (columnas de $\mathbf{V}$ en la SVD de $\mathbf{B}$).
- Sus eigenvalores $\lambda_k = \sigma_k^2/(n-1)$ son las **varianzas** de los datos en cada dirección principal.

## Conexiones

- Habilita: [[principal-component-analysis]]
- Relacionado: [[singular-value-decomposition]], [[singular-values]]

## Fuentes

- [[brunton-kutz-ch1]] §1.5 pp. 54–55
