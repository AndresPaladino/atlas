---
type: example
title: "Parametrización del segmento de recta"
aliases: ["line segment parametrization", "segmento paramétrico"]
areas: [math]
tags: [calculus/vector, curves, examples]
requires: ["[[curve-parametrization]]"]
unlocks: []
bloom: 0
illustrates: ["[[curve-parametrization]]"]
difficulty: 1
sources: []
seen_in_subjects: [calculo-vectorial]
created: 2026-06-04
updated: 2026-06-04
---

# Parametrización del segmento de recta

## Enunciado

Parametrizar el segmento que une los puntos $A, B \in \mathbb{R}^n$.

## Parametrización

$$\gamma(t) = (1-t)\,A + t\,B, \quad t \in [0, 1]$$

En $t = 0$ se está en $A$; en $t = 1$ se está en $B$.

## Vector tangente

$$\gamma'(t) = B - A$$

Es constante: la dirección y la velocidad no cambian a lo largo del segmento.

## Intuición

La parametrización es una interpolación lineal entre $A$ y $B$. El parámetro $t$ representa la fracción del recorrido completado.

## Uso típico

Es la parametrización estándar para calcular [[line-integral]] sobre segmentos rectos. Extendiendo $t \in \mathbb{R}$ se obtiene la recta completa que pasa por $A$ y $B$.

## Conexiones

- Ilustra: [[curve-parametrization]]
- Relacionado: [[line-integral]]
