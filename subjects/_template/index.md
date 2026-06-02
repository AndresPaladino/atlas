---
updated: YYYY-MM-DD
---

# Índice: [Nombre de la Materia]

## Temario del curso
- Tema 1: (completar con temario real del curso)
- Tema 2: (completar con temario real del curso)

## Notación del curso
- (agregar notación específica de la materia)

## Conceptos

### Entiendo
(se completa automáticamente en sesiones)

### Tengo dudas
(se completa automáticamente en sesiones)

## Bloom actual
[Tema principal]: **1** (inicial)

## Sesiones con Claude
| Fecha | Ejercicios / temas trabajados | Resultado |
|---|---|---|
| (se llena automático al cierre de cada sesión) | | |

## Conceptos wiki

```dataview
TABLE bloom, areas, type
FROM "wiki/concepts" OR "wiki/theorems" OR "wiki/methods" OR "wiki/examples"
WHERE contains(seen_in_subjects, regexreplace(this.file.folder, ".*/", ""))
SORT bloom DESC, file.name ASC
```

> Fallback sin Dataview: ver `wiki/index.md` y filtrar por `seen_in_subjects: [<slug-de-esta-materia>]`. La verdad ejecutable del Bloom vive en el frontmatter de cada página wiki — la sección "Bloom actual" de arriba es referencia humana.
