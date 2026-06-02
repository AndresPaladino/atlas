---
type: concept
title: "Punto crítico"
aliases: ["critical point", "punto estacionario", "stationary point"]
areas: [math]
tags: [calculus/vector, optimization]
requires: []
unlocks: ["[[hessian-criterion]]"]
bloom: 2
sources: []
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---

# Punto crítico

## Definición

Sea $f: U \subseteq \mathbb{R}^n \to \mathbb{R}$ diferenciable. Un punto $p \in U$ es **crítico** (o **estacionario**) si $\nabla f(p) = 0$.

## Intuición

Es donde la función no tiene tasa de cambio instantánea en ninguna dirección. Geométricamente: el plano tangente al grafo de $f$ en $(p, f(p))$ es horizontal.

Los puntos críticos son **candidatos** a extremos locales (máximos, mínimos) pero no todos lo son: existen sillas. La clasificación requiere información adicional — típicamente la Hessiana (ver [[hessian-criterion]]).

## Casos

- **Máximo local**: $f(p) \geq f(x)$ para $x$ en un entorno de $p$.
- **Mínimo local**: $f(p) \leq f(x)$ para $x$ en un entorno de $p$.
- **Silla**: en cualquier entorno de $p$ existen $x_1, x_2$ con $f(x_1) > f(p) > f(x_2)$.

## Conexiones

- Habilita: [[hessian-criterion]]
- Aparece en: Cálculo Vectorial, Tema 1.
