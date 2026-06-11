---
type: concept
title: "Randomized SVD (rSVD)"
aliases: ["rSVD", "randomized singular value decomposition", "SVD aleatorizada"]
areas: [linear-algebra, data-science, numerical-analysis]
tags: [linear-algebra/matrix-decomposition, numerical-analysis/algorithms]
requires: ["[[singular-value-decomposition]]", "[[low-rank-approximation]]"]
unlocks: []
sources: ["[[brunton-kutz-ch1]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

La **SVD aleatorizada** es un algoritmo para aproximar la SVD de bajo rango de una matriz grande $\mathbf{X} \in \mathbb{R}^{n \times m}$ (con $n \gg m$) en dos pasos via proyecciones aleatorias [[brunton-kutz-ch1]] §1.8 p. 75:

**Paso 1 — Muestrear el espacio columna:**

$$\mathbf{Z} = \mathbf{X}\mathbf{P}, \qquad \mathbf{P} \in \mathbb{R}^{m \times (r+p)}, \quad \mathbf{Z} = \mathbf{Q}\mathbf{R}.$$

donde $\mathbf{P}$ es una matriz aleatoria (Gaussiana i.i.d.) y $\mathbf{Q}$ se obtiene de la descomposición QR de $\mathbf{Z}$.

**Paso 2 — Proyectar y descomponer:**

$$\mathbf{Y} = \mathbf{Q}^*\mathbf{X}, \quad \mathbf{Y} = \mathbf{U}_Y\boldsymbol{\Sigma}\mathbf{V}^*, \quad \mathbf{U} = \mathbf{Q}\mathbf{U}_Y.$$

## Intuición

Es muy poco probable que una proyección aleatoria $\mathbf{P}$ destruya los componentes dominantes de $\mathbf{X}$. La matriz $\mathbf{Z}$ (mucho más pequeña) aproxima el espacio columna de $\mathbf{X}$, y la SVD se calcula sobre $\mathbf{Y}$ (tamaño $(r+p) \times m$, manejable). El costo total es $\mathcal{O}(nm\log r)$ vs $\mathcal{O}(nm\min(n,m))$ para la SVD exacta.

## Mejoras

- **Oversampling** ($p > 0$): agregar columnas extras a $\mathbf{P}$ (típicamente $p = 5$–$10$) mejora la precisión sustancialmente.
- **Power iterations** ($q$): preprocesar $\mathbf{X}^{(q)} = (\mathbf{X}\mathbf{X}^*)^q\mathbf{X}$ para matrices con espectro de decaimiento lento; requiere $q$ pasadas adicionales sobre $\mathbf{X}$.

## Conexiones

- Requiere: [[singular-value-decomposition]], [[low-rank-approximation]]
- Relacionado: [[eckart-young-theorem]]

## Fuentes

- [[brunton-kutz-ch1]] §1.8 pp. 75–81
