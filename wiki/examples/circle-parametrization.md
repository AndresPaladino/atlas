---
type: example
title: "Parametrización de la circunferencia"
aliases: ["circle parametrization", "circunferencia paramétrica"]
areas: [math]
tags: [calculus/vector, curves, examples]
requires: ["[[curve-parametrization]]"]
unlocks: []
illustrates: ["[[curve-parametrization]]"]
difficulty: 1
sources: []
created: 2026-06-04
updated: 2026-06-04
---

# Parametrización de la circunferencia

## Enunciado

Parametrizar la circunferencia de radio $R$ centrada en el origen.

## Parametrización

$$\gamma(t) = (R\cos t,\; R\sin t), \quad t \in [0, 2\pi]$$

## Vector tangente

$$\gamma'(t) = (-R\sin t,\; R\cos t)$$

El módulo es $\|\gamma'(t)\| = R$ (constante): la circunferencia se recorre a velocidad uniforme.

Como $\gamma'(t) \neq 0$ para todo $t$, no hay cúspides ni tangentes singulares.

## Variantes

- **Sentido horario**: $\gamma(t) = (R\cos t,\; -R\sin t)$.
- **Centro en $(a, b)$**: $\gamma(t) = (a + R\cos t,\; b + R\sin t)$.
- **Elipse**: $\gamma(t) = (a\cos t,\; b\sin t)$ con semiejes $a$ y $b$.

## Conexiones

- Ilustra: [[curve-parametrization]]
- Relacionado: [[arc-length]] (el arco de $0$ a $\theta$ es $R\theta$)
