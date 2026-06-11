---
type: concept
title: "Jacobiano"
aliases: ["Jacobian", "matriz Jacobiana", "Jφ", "Dφ"]
areas: [math]
tags: [calculus/vector, differentiation]
requires: []
unlocks: ["[[implicit-function-theorem]]"]
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Jacobiano

## Definición

Sea $\varphi: U \subseteq \mathbb{R}^n \to \mathbb{R}^m$ diferenciable. La **matriz Jacobiana** de $\varphi$ en $p$ es la matriz $m \times n$ de derivadas parciales:

$$J\varphi(p) = D\varphi(p) = \begin{pmatrix}
\frac{\partial \varphi_1}{\partial x_1} & \cdots & \frac{\partial \varphi_1}{\partial x_n} \\
\vdots & & \vdots \\
\frac{\partial \varphi_m}{\partial x_1} & \cdots & \frac{\partial \varphi_m}{\partial x_n}
\end{pmatrix}_{p}$$

Cuando $m = n$, el **determinante Jacobiano** $\det J\varphi(p)$ se llama también "el Jacobiano" — sin matriz.

## Intuición

$J\varphi(p)$ es la mejor aproximación lineal a $\varphi$ cerca de $p$: $\varphi(p + h) \approx \varphi(p) + J\varphi(p) \, h$.

Cuando $m = n$ y $\det J\varphi(p) \neq 0$, $\varphi$ es localmente invertible cerca de $p$ (teorema de la función inversa). El determinante también gobierna el cambio de área/volumen bajo transformaciones (cambio de variables en integrales).

## Deducción de $D\varphi$ por regla de la cadena

Si $F(x, \varphi(x)) = 0$ identicamente (caso TFI), derivando ambos lados respecto a $x$:

$$\frac{\partial F}{\partial x} + \frac{\partial F}{\partial y} D\varphi = 0$$

Despejando:

$$D\varphi = -\left[\frac{\partial F}{\partial y}\right]^{-1} \frac{\partial F}{\partial x}.$$

Esto es la fórmula que aparece en el [[implicit-function-theorem]].

## Conexiones

- Habilita: [[implicit-function-theorem]]
- Relacionado con: cambio de variables en integrales múltiples (Tema 5-9 de Cálc Vect).
- Aparece en: Cálculo Vectorial, Temas 2 y siguientes.
