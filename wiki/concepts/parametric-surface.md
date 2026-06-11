---
type: concept
title: "Superficie paramétrica"
aliases: ["parametric surface", "superficie parametrizada", "parametrización de superficie"]
areas: [math]
tags: [calculus/vector, surfaces]
requires: ["[[curve-parametrization]]", "[[jacobian]]"]
unlocks: ["[[surface-integral]]"]
sources: ["[[gonzalez-cvec-2023]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Una **superficie paramétrica** en $\mathbb{R}^3$ es la imagen de una función continua

$$\Phi: (u,v) \in D \subset \mathbb{R}^2 \to \Phi(u,v) = (x(u,v), y(u,v), z(u,v)) \in \mathbb{R}^3.$$

$D$ es la región paramétrica y $S = \text{Im}(\Phi)$ [[gonzalez-cvec-2023]] §2.5 p. 70.

## Regularidad y plano tangente

$\Phi$ es **regular** en $A = (u_0, v_0)$ si $\Phi_u(A) \wedge \Phi_v(A) \neq \mathbf{0}$.

En un punto regular, el espacio de vectores tangentes es el plano

$$T_P S : (X - P) \cdot (\Phi_u(A) \wedge \Phi_v(A)) = 0$$

generado por $\Phi_u(A)$ y $\Phi_v(A)$ [[gonzalez-cvec-2023]] §2.5.1 p. 75.

## Área de una superficie parametrizada

$$A(S) = \iint_D \|\Phi_u(u,v) \wedge \Phi_v(u,v)\|\, \mathrm{d}u\, \mathrm{d}v.$$

Para la gráfica $z = f(x,y)$: $A(S) = \iint_D \sqrt{1 + f_x^2 + f_y^2}\, \mathrm{d}x\, \mathrm{d}y$ [[gonzalez-cvec-2023]] §2.5.2 p. 78.

## Ejemplos canónicos

- Esfera de radio $r$: $\Phi(u,v) = (r\cos u\sin v, r\sin u\sin v, r\cos v)$, área $4\pi r^2$.
- Toro con radios $a > b$: área $4\pi^2 ab$.
- Superficie de revolución: se gira una curva $\alpha(t) = (x(t), 0, z(t))$ alrededor del eje $Oz$.

## Conexiones

- Requiere: [[curve-parametrization]], [[jacobian]]
- Habilita: [[surface-integral]]
- Relacionado: [[arc-length]] (longitud de arco es el análogo 1D del área de superficie)
