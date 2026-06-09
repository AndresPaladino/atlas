---
type: example
title: "Parametrización de la hélice"
aliases: ["helix parametrization", "hélice", "helical curve"]
areas: [math]
tags: [calculus/vector, curves, examples]
requires: ["[[curve-parametrization]]"]
unlocks: []
bloom: 0
illustrates: ["[[curve-parametrization]]"]
difficulty: 2
sources: []
seen_in_subjects: [calculo-vectorial]
created: 2026-06-04
updated: 2026-06-04
---

# Parametrización de la hélice

## Enunciado

La hélice circular estándar es la curva en $\mathbb{R}^3$ que sube uniformemente en $z$ mientras gira en el plano $xy$.

## Parametrización

$$\gamma(t) = (\cos t,\; \sin t,\; t), \quad t \in \mathbb{R}$$

Con radio $R$ y paso $h$ por vuelta completa:

$$\gamma(t) = \left(R\cos t,\; R\sin t,\; \frac{h}{2\pi}\,t\right)$$

## Vector tangente

$$\gamma'(t) = (-\sin t,\; \cos t,\; 1)$$

El módulo es $\|\gamma'(t)\| = \sqrt{\sin^2 t + \cos^2 t + 1} = \sqrt{2}$ (constante para la hélice unitaria).

## Intuición

La proyección de la hélice sobre el plano $xy$ es una circunferencia. La componente $z = t$ hace que la curva "suba" a velocidad constante. Es el prototipo de curva en $\mathbb{R}^3$ para cálculos de [[arc-length]] en tres dimensiones.

## Longitud de arco

Para la hélice unitaria entre $t = 0$ y $t = 2\pi$ (una vuelta completa):

$$L = \int_0^{2\pi} \|\gamma'(t)\|\,\mathrm{d}t = \int_0^{2\pi} \sqrt{2}\,\mathrm{d}t = 2\pi\sqrt{2}$$

## Conexiones

- Ilustra: [[curve-parametrization]]
- Relacionado: [[arc-length]]
