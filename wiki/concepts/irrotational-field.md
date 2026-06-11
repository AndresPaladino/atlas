---
type: concept
title: "Campo irrotacional"
aliases: ["irrotational field", "campo de rotor nulo", "curl-free field"]
areas: [math]
tags: [calculus/vector, fields]
requires: ["[[curl]]", "[[gradient-field]]"]
unlocks: []
sources: ["[[gonzalez-cvec-2023]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Un campo vectorial $X: U \subset \mathbb{R}^3 \to \mathbb{R}^3$ de clase $C^1$ es **irrotacional** en $U$ si $\text{rot}\, X = \mathbf{0}$ en todo $U$ [[gonzalez-cvec-2023]] §2.7.2 p. 99.

## Relación con campos de gradientes

Todo campo de gradientes ($X = \nabla f$) es irrotacional, ya que $\nabla \times \nabla f = \mathbf{0}$.

El recíproco depende de la topología de $U$:
- Si $U$ es **simplemente conexo**, entonces irrotacional $\Rightarrow$ campo de gradientes.
- Si $U$ tiene "agujeros" (no es simplemente conexo), un campo puede ser irrotacional sin ser de gradientes. Ejemplo clásico: $X = \left(\frac{-y}{x^2+y^2}, \frac{x}{x^2+y^2}, 0\right)$ en $\mathbb{R}^3 \setminus \{$eje $z\}$.

## Conexiones

- Requiere: [[curl]], [[gradient-field]]
- Relacionado: [[solenoidal-field]] (concepto análogo con la divergencia)
