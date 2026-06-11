---
type: method
title: "Análisis de Kleene"
aliases: ["Kleene analysis", "método de Kleene", "análisis Kleene"]
areas: [computing]
tags: [formal-languages, automata, regular-languages]
requires: ["[[finite-automaton]]", "[[regular-expression]]", "[[arden-lemma]]"]
unlocks: []
when_to_use: "Para extraer la expresión regular reconocida por un autómata finito (AFD o AFND). Se plantea un sistema de ecuaciones desde las transiciones salientes de cada estado y se resuelve usando el lema de Arden."
fails_when: "No falla en términos de existencia (todo autómata finito reconoce un lenguaje regular), pero el sistema puede volverse pesado si el autómata tiene muchos estados con interconexiones densas — se recomienda primero minimizar."
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Análisis de Kleene

## Cuándo se usa

Para obtener la expresión regular que describe el lenguaje aceptado por un [[finite-automaton]]. Es la dirección "autómata → ER" de la equivalencia entre autómatas finitos y lenguajes regulares.

## Procedimiento

Dado un autómata con estados $q_0, q_1, \ldots, q_n$ donde $q_0$ es inicial y $F \subseteq \{q_0, \ldots, q_n\}$ son finales:

1. Para cada estado $q_i$, definir una variable $X_i$ que representa el conjunto de cadenas que llevan desde $q_i$ hasta un estado final.
2. Plantear una ecuación para $X_i$ a partir de las **transiciones salientes** desde $q_i$:
   $$X_i = a_1 X_{j_1} \mid a_2 X_{j_2} \mid \cdots \mid \varepsilon \text{ (si } q_i \in F\text{)}$$
   donde $a_k$ es el símbolo que va de $q_i$ a $q_{j_k}$.
3. Resolver el sistema. Sustituir hacia atrás, eliminando variables. Cuando una ecuación tiene la forma $X = rX \mid s$ (con $r$ no aceptando $\varepsilon$), aplicar [[arden-lemma]]: $X = r^* s$.
4. La expresión final del lenguaje aceptado es $X_0$ (la variable del estado inicial).

## Convenciones

- $\varepsilon$ aparece en la ecuación de $X_i$ **si y solo si** $q_i \in F$.
- El **estado pozo** (sumidero no final) se puede omitir: su variable es $\emptyset$, contribuye con nada.
- Si hay múltiples estados finales: cada uno aporta $\varepsilon$ a su propia ecuación.

## Notación estricta de ER

- Concatenación: yuxtaposición o `.` ($a \cdot b$ o $ab$).
- Alternancia: `|`.
- Estrella de Kleene: $r^*$.
- **No** usar `+` para "una o más" — escribir $r \cdot r^*$ en su lugar.
- Factorización: $b \mid aa^* b = a^* b$ (factor común a derecha).

## Conexiones

- Requiere: [[finite-automaton]], [[regular-expression]], [[arden-lemma]]
- Aparece en: Teoría de Lenguajes, Tema 1 (Lenguajes Regulares).
