---
type: concept
title: "Autómata finito"
aliases: ["finite automaton", "AF", "AFD", "AFND", "DFA", "NFA"]
areas: [computing]
tags: [formal-languages, automata, regular-languages]
requires: []
unlocks: ["[[kleene-analysis]]"]
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Autómata finito

## Definición

Un **autómata finito determinista (AFD)** es una tupla $M = (Q, \Sigma, \delta, q_0, F)$ donde:

- $Q$ es un conjunto finito de estados.
- $\Sigma$ es el alfabeto de entrada.
- $\delta: Q \times \Sigma \to Q$ es la función de transición.
- $q_0 \in Q$ es el estado inicial.
- $F \subseteq Q$ es el conjunto de estados finales (de aceptación).

Un **autómata finito no determinista (AFND)** generaliza con $\delta: Q \times \Sigma \to 2^Q$. Una variante (AFND-$\varepsilon$) admite transiciones $\varepsilon$ (sin consumir símbolo).

## Aceptación de una cadena

$M$ acepta $w \in \Sigma^*$ si existe una secuencia de transiciones leyendo $w$ desde $q_0$ que termina en un estado de $F$.

El **lenguaje aceptado** es $L(M) = \{w \in \Sigma^* : M \text{ acepta } w\}$.

## Equivalencia entre modelos

- AFD, AFND, y AFND-$\varepsilon$ reconocen exactamente la misma clase de lenguajes (los **regulares**). Construcciones:
  - AFND → AFD: construcción de subconjuntos (potencia).
  - AFND-$\varepsilon$ → AFND: clausura $\varepsilon$.
- Equivalencia con [[regular-expression]]: teorema de Kleene.

## Estado pozo

Estado sin salida hacia ningún estado final. Se puede omitir al dibujar el autómata sin alterar el lenguaje aceptado.

## Autómata mínimo

Todo lenguaje regular tiene un AFD único (salvo isomorfismo) con el menor número de estados. Algoritmos clásicos: partición por equivalencias (Hopcroft, Moore).

## Conexiones

- Equivalente a: [[regular-expression]]
- Habilita: [[kleene-analysis]] (para extraer la ER desde un autómata).
- Aparece en: Teoría de Lenguajes, Tema 1 (Lenguajes Regulares).
