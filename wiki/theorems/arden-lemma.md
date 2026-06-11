---
type: theorem
title: "Lema de Arden"
aliases: ["Arden's lemma", "Arden", "lema Arden"]
areas: [computing]
tags: [formal-languages, regular-languages]
requires: ["[[regular-expression]]"]
unlocks: ["[[kleene-analysis]]"]
statement_form: "Si X = rX | s (sobre expresiones regulares) y r no acepta la palabra vacía, entonces X = r*.s es la solución única."
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Lema de Arden

## Enunciado (versión Kleene)

Sea una ecuación sobre expresiones regulares:

$$X = r X \mid s$$

donde $r$ y $s$ son expresiones regulares y $r$ **no acepta** la palabra vacía $\varepsilon$. Entonces la única solución es:

$$X = r^* \cdot s.$$

## Intuición

Si $X$ es el lenguaje que satisface $X = rX \mid s$, entonces una cadena $w \in X$ es:
- una cadena de $s$ directamente, o
- una cadena de $r$ seguida por otra cadena de $X$.

Iterando: $w$ es 0 o más prefijos en $r$ seguidos de un sufijo en $s$. Eso es exactamente $r^* s$.

La condición $\varepsilon \notin r$ asegura unicidad: si $\varepsilon \in r$ entonces cualquier $X' \supseteq r^* s$ también satisface la ecuación, y la solución no es única.

## Uso

Es la herramienta de cierre para el [[kleene-analysis]]: al sustituir variables en el sistema de ecuaciones, las recursiones de la forma $X = rX \mid s$ se resuelven aplicando este lema.

## Conexiones

- Requiere: [[regular-expression]]
- Habilita: [[kleene-analysis]]
- Aparece en: Teoría de Lenguajes, Tema 1 (Lenguajes Regulares).
