---
type: concept
title: "Unitary Matrix"
aliases: ["matriz unitaria", "orthogonal matrix", "matriz ortogonal"]
areas: [linear-algebra]
tags: [linear-algebra/matrix-properties]
requires: []
unlocks: ["[[singular-value-decomposition]]"]
sources: ["[[brunton-kutz-ch1]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Una matriz cuadrada $\mathbf{U} \in \mathbb{C}^{n \times n}$ es **unitaria** si

$$\mathbf{U}\mathbf{U}^* = \mathbf{U}^*\mathbf{U} = \mathbf{I}_n,$$

donde $^*$ denota la transpuesta conjugada [[brunton-kutz-ch1]] §1.1 p. 31. Para matrices reales, la condición se reduce a $\mathbf{U}\mathbf{U}^T = \mathbf{I}$, y la matriz se llama **ortogonal**.

## Intuición

Las matrices unitarias representan rotaciones (y reflexiones) en el espacio complejo: preservan la norma de vectores y el producto interno. Multiplicar por una matriz unitaria es computacionalmente barato de invertir, ya que $\mathbf{U}^{-1} = \mathbf{U}^*$ (solo requiere transponer y conjugar, $\mathcal{O}(n^2)$ en vez de $\mathcal{O}(n^3)$).

## Propiedades

- Las columnas de $\mathbf{U}$ forman una base ortonormal.
- $|\det(\mathbf{U})| = 1$.
- Los eigenvalores de una matriz unitaria tienen módulo 1.
- La SVD garantiza que $\mathbf{U}$ y $\mathbf{V}$ sean unitarias para cualquier $\mathbf{X}$, lo cual hace a la SVD numericamente estable [[brunton-kutz-ch1]] §1.3 p. 43.

## Conexiones

- Habilita: [[singular-value-decomposition]]
- Relacionado: [[pseudo-inverse]] (invertir $\mathbf{U}$ es gratis)

## Fuentes

- [[brunton-kutz-ch1]] §1.1 p. 31, §1.3 p. 43
