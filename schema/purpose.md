---
type: schema
updated: 2026-06-17
---

# Propósito del wiki

Mientras `wiki-conventions.md` y los protocolos definen **cómo** se organiza Atlas,
este archivo define **qué** debe contener y **para qué** — la intención direccional.
Lo leen `/ingest` (decidir qué entra y qué se descarta) y `/query` (entender el
alcance de lo que se puede responder). No se lee por sesión: es referencia bajo demanda.

> Plantilla. Reemplazá cada sección con tu propósito, alcance y preguntas reales.
> Es tu intención, no una regla del sistema.

## Objetivo

⟨Una o dos frases: qué es este grafo de conocimiento y para qué lo usás
(consultar, ejercitar, sintetizar fuentes, etc.).⟩

## Alcance

Dentro (las áreas que declarás en el frontmatter `areas:`):

- `⟨area-1⟩` — ⟨qué cubre⟩
- `⟨area-2⟩` — ⟨qué cubre⟩

Fuera (no ingerir):

- ⟨material que explícitamente no querés en el wiki: administrativo, efímero,
  sin valor reutilizable, etc.⟩

## Preguntas clave que el wiki debe poder responder

- ⟨pregunta tipo 1⟩
- ⟨pregunta tipo 2⟩

## Tesis evolutiva (qué priorizar / podar)

- Priorizar **conexiones** sobre acumulación: una página nueva vale más si engancha con el grafo existente (`requires`/`unlocks`) que aislada.
- Preferir **profundidad conceptual** sobre cobertura exhaustiva: mejor pocas páginas sólidas que muchos stubs.
- Podar lo que no se consulta ni conecta. Un tipo de página sin uso real es candidato a eliminarse del schema.
