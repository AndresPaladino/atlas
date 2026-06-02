---
type: concept
title: "Campo solenoidal"
aliases: ["solenoidal field", "divergence-free field", "campo de divergencia nula", "campo incompresible"]
areas: [math]
tags: [calculus/vector, fields]
requires: ["[[divergence]]"]
unlocks: []
bloom: 0
sources: ["[[gonzalez-cvec-2023]]"]
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Un campo vectorial $X: U \subset \mathbb{R}^3 \to \mathbb{R}^3$ de clase $C^1$ es **solenoidal** en $U$ si $\text{div}\, X = 0$ en todo $U$ [[gonzalez-cvec-2023]] §2.8.2 p. 104.

## Intuición

En un campo de velocidades de fluido, solenoidal equivale a **incompresible**: no hay fuentes ni sumideros; el volumen de cualquier porción del fluido se conserva al moverse.

## Relación con potencial vectorial

Análogamente a cómo un campo irrotacional admite potencial escalar (bajo condiciones topológicas), un campo solenoidal admite un **potencial vectorial** $A$ tal que $X = \nabla \times A$, bajo condiciones similares.

La identidad $\text{div}(\nabla \times A) = 0$ asegura que todo campo con potencial vectorial es solenoidal.

## Conexiones

- Requiere: [[divergence]]
- Relacionado: [[irrotational-field]] (concepto análogo con el rotor), [[gauss-theorem]]
