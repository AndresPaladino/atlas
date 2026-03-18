# Atlas

Sistema de estudio personal para ingeniería, construido sobre [Claude Code](https://claude.ai/code).

Atlas organiza el cursado por materia, guía las sesiones de práctica con método socrático, y lleva un registro automático del progreso usando la taxonomía de Bloom.

---

## Cómo funciona

Abrís este repositorio en Claude Code. Claude lee el `CLAUDE.md` y sabe exactamente cómo comportarse: no te da soluciones directas, te guía para que llegues solo, y al cerrar la sesión actualiza el log y el nivel de Bloom de cada tema.

```
Vos tipeas un paso → Claude evalúa → pista si estás trabado → cierre automático de sesión
```

---

## Estructura

```
Atlas/
├── CLAUDE.md                    ← comportamiento del sistema (Claude lo lee automáticamente)
├── profile/
│   └── student_profile.md       ← tu carrera, materias activas y preferencias
├── subjects/
│   ├── _template/
│   │   └── index.md             ← plantilla para nuevas materias
│   └── [materia]/
│       └── index.md             ← temario, notación, nivel Bloom, log de sesiones
├── archive/                     ← materias finalizadas (contenido local, no en git)
└── logs/                        ← logs de sesión por mes (contenido local, no en git)
```

---

## Setup

### Requisitos
- [Claude Code](https://claude.ai/code) instalado

### Instalación

```bash
git clone https://github.com/TU_USUARIO/atlas.git
cd atlas
bash setup.sh
```

`setup.sh` hace dos cosas:
1. Actualiza los paths en `.claude/settings.local.json` con tu directorio local
2. Crea el directorio de logs del mes actual (`logs/YYYY-MM/`)

---

## Agregar una materia

```bash
cp subjects/_template/index.md subjects/[nombre-materia]/index.md
```

Luego:
1. Editá `subjects/[nombre-materia]/index.md` con el temario y la notación del curso
2. Agregá la materia a `profile/student_profile.md` bajo "Materias activas"

---

## Comenzar una sesión

Abrí Claude Code en el directorio de Atlas:

```bash
claude
```

Claude va a leer `CLAUDE.md` y `profile/student_profile.md` automáticamente. Decile qué tema o ejercicio querés trabajar y empieza la sesión.

---

## Al cerrar una sesión

Claude actualiza automáticamente:
- La tabla de sesiones en `subjects/[materia]/index.md`
- El nivel de Bloom del tema trabajado
- El campo `updated:` del frontmatter

---

## Personalización

Podés modificar `CLAUDE.md` para ajustar el comportamiento del sistema:
- Cambiar el idioma
- Modificar las reglas socráticas
- Ajustar la escala de Bloom
- Agregar convenciones de notación globales

---

## Licencia

MIT — libre para usar, adaptar y compartir.
