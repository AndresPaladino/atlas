---
type: method
title: Versor normal a una superficie paramétrica
aliases:
  - normal vector parametric surface
  - vector normal superficie
  - normal unitario superficie
areas:
  - math
tags:
  - calculus/vector
  - surfaces
requires:
  - "[[parametric-surface]]"
unlocks:
  - "[[surface-integral]]"
when_to_use: 'Cuando se necesita el vector normal unitario a una superficie en un punto dado su parametrización $\Phi(u,v)$.'
fails_when: 'El punto no es regular, es decir $\Phi_u \wedge \Phi_v = \mathbf{0}$; no existe plano tangente definido.'
sources:
  - "[[gonzalez-cvec-2023]]"
created: 2026-06-02
updated: 2026-06-02
---

## Cuándo usarlo

Cuando se tiene una [[parametric-surface]] $\Phi(u,v)$ y se necesita el versor normal en un punto $P = \Phi(u_0, v_0)$. Aparece sistemáticamente en la integral de superficie de un campo vectorial (flujo).

## Procedimiento

**Paso 1 — Vectores tangentes.**

Calcular las derivadas parciales de $\Phi$ en $A = (u_0, v_0)$:

$$\Phi_u(A) = \left(\frac{\partial x}{\partial u},\, \frac{\partial y}{\partial u},\, \frac{\partial z}{\partial u}\right), \qquad \Phi_v(A) = \left(\frac{\partial x}{\partial v},\, \frac{\partial y}{\partial v},\, \frac{\partial z}{\partial v}\right).$$

Estos dos vectores generan el plano tangente a $S$ en $P$.

**Paso 2 — Vector normal (no unitario).**

$$\mathbf{N}(A) = \Phi_u(A) \wedge \Phi_v(A).$$

$\mathbf{N}$ es ortogonal al plano tangente. La condición $\mathbf{N}(A) \neq \mathbf{0}$ es exactamente la definición de punto regular de [[parametric-surface]].

**Paso 3 — Normalizar.**

$$\hat{n}(A) = \frac{\mathbf{N}(A)}{\|\mathbf{N}(A)\|}.$$

## Orientación

Tanto $\hat{n}$ como $-\hat{n}$ son versores normales válidos; la elección fija la **orientación** de la superficie. En [[surface-integral]] de flujo, el signo del resultado depende de qué normal se elija — hay que declararlo explícitamente o inferirlo del contexto geométrico (ej: normal exterior en una superficie cerrada).

## Cuándo falla

Si $\Phi_u(A) \wedge \Phi_v(A) = \mathbf{0}$, el punto $A$ es singular: los vectores tangentes son paralelos o uno es cero, y no hay plano tangente definido. El método no aplica en ese punto.

## Conexiones

- Requiere: [[parametric-surface]]
- Habilita: [[surface-integral]]
- Relacionado: [[curl]], [[gauss-theorem]], [[stokes-theorem]]
