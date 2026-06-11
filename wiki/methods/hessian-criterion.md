---
type: method
title: "Criterio de la Hessiana"
aliases: ["Hessian criterion", "criterio de segundas derivadas", "test de la Hessiana"]
areas: [math]
tags: [calculus/vector, optimization, critical-points]
requires: ["[[critical-point]]"]
unlocks: []
when_to_use: "Para clasificar un punto crítico de una función escalar $C^2$ en varias variables como máximo, mínimo o silla, cuando la Hessiana evaluada en el punto es no singular."
fails_when: "$\\det H_f(p) = 0$ (Hessiana singular): el criterio no decide. Hay que recurrir a análisis por definición, restricción a curvas, o desarrollos de Taylor de orden superior."
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Criterio de la Hessiana

## Cuándo se usa

Dado $f: U \subseteq \mathbb{R}^n \to \mathbb{R}$ de clase $C^2$ y un punto crítico $p$ (con $\nabla f(p) = 0$), se quiere clasificar $p$ como máximo local, mínimo local, o punto silla. La Hessiana $H_f(p)$ es la matriz de segundas derivadas parciales evaluada en $p$.

## Cuándo falla

El criterio no decide cuando $\det H_f(p) = 0$ — la información de segundo orden es insuficiente. Alternativas:

- **Análisis por definición**: estudiar $f(x) - f(p)$ cerca de $p$.
- **Restricción a curvas**: evaluar $f$ a lo largo de varias curvas que pasen por $p$ y comparar.
- **Taylor de orden superior**: si $f$ es $C^k$, el primer término no nulo del desarrollo decide.

## Enunciado (caso $n=2$)

Para $f: \mathbb{R}^2 \to \mathbb{R}$ con $p$ crítico:

- $\det H_f(p) > 0$ y $f_{xx}(p) > 0$ → mínimo local.
- $\det H_f(p) > 0$ y $f_{xx}(p) < 0$ → máximo local.
- $\det H_f(p) < 0$ → silla.
- $\det H_f(p) = 0$ → no decide.

Caso general $n > 2$: clasificar $H_f(p)$ por signos de sus autovalores (definida positiva / negativa / indefinida).

## Conexiones

- Requiere: [[critical-point]]
- Aparece en: Cálculo Vectorial, Tema 1 (Extremos relativos).
