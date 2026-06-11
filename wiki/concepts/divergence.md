---
type: concept
title: "Divergencia"
aliases: ["divergence", "div", "∇·F"]
areas: [math]
tags: [calculus/vector, fields, differential-operators]
requires: ["[[jacobian]]"]
unlocks: ["[[solenoidal-field]]", "[[gauss-theorem]]"]
sources: ["[[gonzalez-cvec-2023]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Para un campo vectorial $X = (P, Q, R): U \subset \mathbb{R}^3 \to \mathbb{R}^3$ de clase $C^1$, la **divergencia** de $X$ es [[gonzalez-cvec-2023]] §2.8.1 p. 102:

$$\text{div}\, X = \nabla \cdot X = \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} + \frac{\partial R}{\partial z}.$$

El resultado es un **campo escalar**.

## Intuición

La divergencia mide la **expansión o compresión local** del campo. Si $X$ es un campo de velocidades de un fluido:
- $\text{div}\, X > 0$ en un punto: el fluido se expande (fuente).
- $\text{div}\, X < 0$: el fluido se comprime (sumidero).
- $\text{div}\, X = 0$: sin producción ni absorción local. Ver [[solenoidal-field]].

## Relación con el Teorema de Gauss

La divergencia aparece en [[gauss-theorem]] (Teorema de la Divergencia):

$$\iiint_V \text{div}\, X\, \mathrm{d}V = \oiint_{\partial V} X \cdot \mathrm{d}S.$$

## Conexiones

- Requiere: [[jacobian]]
- Habilita: [[solenoidal-field]], [[gauss-theorem]]
- Relacionado: [[curl]] (el análogo vectorial de la divergencia)
