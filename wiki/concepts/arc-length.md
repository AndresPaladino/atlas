---
type: concept
title: "Longitud de arco"
aliases: ["arc length", "longitud de curva", "arc-length parametrization"]
areas: [math]
tags: [calculus/vector, curves]
requires: ["[[curve-parametrization]]"]
unlocks: ["[[line-integral]]"]
bloom: 0
sources: ["[[gonzalez-cvec-2023]]"]
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Dada una curva paramétrica de clase $C^1$, $\alpha: [a,b] \to \mathbb{R}^n$, la **longitud de arco** de $\alpha$ entre $a$ y $b$ es:

$$L_a^b(\alpha) = \int_a^b \|\alpha'(t)\|\, \mathrm{d}t.$$

En $\mathbb{R}^3$ con $\alpha(t) = (x(t), y(t), z(t))$:

$$L_a^b(\alpha) = \int_a^b \sqrt{x'(t)^2 + y'(t)^2 + z'(t)^2}\, \mathrm{d}t.$$

## Invarianza por reparametrización

La longitud no depende de la parametrización elegida: si $\beta = \alpha \circ \varphi$ es una reparametrización con $\varphi: [c,d] \to [a,b]$ difeomorfismo, entonces $L_c^d(\beta) = L_a^b(\alpha)$ [[gonzalez-cvec-2023]] §2.1.2 p. 46.

## Parametrización por longitud de arco

Una curva está **parametrizada por longitud de arco** si $\|\alpha'(s)\| = 1$ para todo $s$. Esto equivale a que $L_0^s(\alpha) = s$.

Toda curva regular admite reparametrización por longitud de arco: se define $L(t) = \int_{t_0}^t \|\alpha'(\tau)\|\mathrm{d}\tau$, que es un difeomorfismo creciente, y se toma $\beta = \alpha \circ L^{-1}$ [[gonzalez-cvec-2023]] §2.1.3 p. 46.

La parametrización por longitud de arco es la canónica para estudiar curvatura y el triedro de Frenet.

## Conexiones

- Requiere: [[curve-parametrization]]
- Habilita: [[line-integral]]
- Relacionado: [[parametric-surface]] (área de superficie es el análogo 2D)
