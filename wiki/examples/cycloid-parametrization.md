---
type: example
title: "Parametrización de la cicloide"
aliases: ["cicloide", "cycloid"]
areas: [math]
tags: [calculus/vector, curves, examples]
requires: []
unlocks: []
bloom: 2
illustrates: ["[[curve-parametrization]]"]
difficulty: 2
session_ref: "subjects/calculo-vectorial/index.md#2026-04-19"
sources: []
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---

# Parametrización de la cicloide

## Enunciado

La cicloide es la curva descrita por un punto fijo en el borde de un círculo de radio $R$ que rueda sin deslizar sobre una recta horizontal.

## Deducción geométrica

Sea $\theta$ el ángulo girado por el círculo desde su posición inicial. La condición de rodadura sin deslizamiento implica que el centro del círculo está en $(R\theta, R)$ (el arco recorrido $R\theta$ iguala el desplazamiento horizontal).

El punto fijo, que partió desde $(0, 0)$, está rotado respecto al centro un ángulo $-\theta$ (sentido horario relativo). Sus coordenadas:

$$\gamma(\theta) = (R\theta - R\sin\theta, \; R - R\cos\theta) = R(\theta - \sin\theta, \; 1 - \cos\theta).$$

## Tangentes y singularidades

Derivando:

$$\gamma'(\theta) = R(1 - \cos\theta, \; \sin\theta).$$

- $\gamma'(\theta) = 0 \iff 1 - \cos\theta = 0$ y $\sin\theta = 0 \iff \theta = 2k\pi$.
- En $\theta = 2k\pi$: ambas derivadas se anulan → **cúspide**. Coincide con el punto del círculo que toca el piso (y reinicia el ciclo).
- Tangente horizontal ($y'(\theta) = 0$ con $x'(\theta) \neq 0$): $\sin\theta = 0$ y $1 - \cos\theta \neq 0$ → $\theta = (2k+1)\pi$. Es el punto más alto del arco.

## Variantes

- **Cicloide acortada**: el punto fijo está a distancia $r < R$ del centro (no en el borde). No hay cúspides — la curva no toca el piso.
- **Cicloide alargada**: el punto fijo está a distancia $r > R$ del centro (extendido más allá del borde). Hay lazos.

## Conexiones

- Ilustra: [[curve-parametrization]]
- Trabajado en sesión: ver `subjects/calculo-vectorial/index.md` entrada 2026-04-19.
