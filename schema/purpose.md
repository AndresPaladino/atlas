---
type: schema
updated: 2026-06-17
---

# Propósito del wiki

Mientras `wiki-conventions.md` y los protocolos definen **cómo** se organiza Atlas,
este archivo define **qué** debe contener y **para qué** — la intención direccional.
Lo leen `/ingest` (decidir qué entra y qué se descarta) y `/query` (entender el
alcance de lo que se puede responder). No se lee por sesión: es referencia bajo demanda.

> Borrador inicial inferido del contenido actual. Editalo: es tu intención, no una regla del sistema.

## Objetivo

Un grafo de conocimiento personal sobre el material de la carrera (Fing / UdelaR):
capturar la **síntesis conceptual** —definiciones, intuición, teoremas, métodos y sus
conexiones— de modo que sea consultable (`/query`) y ejercitable (`/practice`), con
trazabilidad a las fuentes que lo justifican.

## Alcance

Dentro (las 5 áreas, ver `areas:` del frontmatter):

- `math` — cálculo vectorial, álgebra lineal, geometría diferencial, etc.
- `signals` — procesamiento de señales y sistemas.
- `computing` — teoría de la computación, sistemas operativos, programación concurrente.
- `engineering-physics` — física para ingeniería.
- `ml` — machine learning y data science.

Fuera (no ingerir):

- Material administrativo, fechas, logística de cursos.
- Contenido sin valor reutilizable (apuntes de una sola clase sin conceptos transferibles).
- Resoluciones de exámenes completas como tales — sí los conceptos/métodos que ilustran.

## Preguntas clave que el wiki debe poder responder

- ¿Qué es X, cuál es su intuición y de qué depende (`requires`)?
- ¿Qué teorema/método aplica a este problema y cuándo falla?
- ¿Cómo se conectan dos temas de áreas distintas?
- ¿Qué fuente justifica esta afirmación y en qué página?

## Tesis evolutiva (qué priorizar / podar)

- Priorizar **conexiones** sobre acumulación: una página nueva vale más si engancha con el grafo existente (`requires`/`unlocks`) que aislada.
- Preferir **profundidad conceptual** sobre cobertura exhaustiva: mejor pocas páginas sólidas que muchos stubs.
- Podar lo que no se consulta ni conecta. Un tipo de página sin uso real (p. ej. `comparison`, hoy vacío) es candidato a eliminarse del schema.
