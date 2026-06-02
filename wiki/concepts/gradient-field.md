---
type: concept
title: "Campo de gradientes"
aliases: ["gradient field", "campo conservativo", "conservative field", "campo potencial", "potential field"]
areas: [math]
tags: [calculus/vector, integration, fields]
requires: ["[[line-integral]]"]
unlocks: ["[[greens-theorem]]", "[[irrotational-field]]"]
bloom: 0
sources: ["[[gonzalez-cvec-2023]]"]
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Un campo vectorial $X: U \subset \mathbb{R}^n \to \mathbb{R}^n$ continuo es un **campo de gradientes** si existe $f: U \to \mathbb{R}$ de clase $C^1$ tal que $X = \nabla f$ en $U$. Se dice que $f$ es un **potencial escalar** de $X$ en $U$ [[gonzalez-cvec-2023]] §2.3 p. 57.

## Propiedad fundamental (Regla de Barrow para integrales de línea)

Si $X = \nabla f$ y $C$ es una curva en $U$ desde $A$ hasta $B$ [[gonzalez-cvec-2023]] §2.3.1 p. 59:

$$\int_C X \cdot \mathrm{d}s = f(B) - f(A).$$

En particular, si $C$ es cerrada: $\oint_C X \cdot \mathrm{d}s = 0$.

Consecuencia: la integral de línea de un campo conservativo **no depende del camino**, solo de los extremos.

## Unicidad del potencial

Si $U$ es abierto y conexo, dos potenciales de $X$ difieren en una constante [[gonzalez-cvec-2023]] §2.3 p. 58.

## Observación importante

La existencia de un potencial escalar depende tanto del campo $X$ como del dominio $U$ donde está definido. El mismo campo puede ser de gradientes en un subconjunto pero no en otro.

## Conexiones

- Requiere: [[line-integral]]
- Habilita: [[greens-theorem]], [[irrotational-field]]
- Relacionado: [[curl]] (un campo de gradientes tiene rotor nulo)
