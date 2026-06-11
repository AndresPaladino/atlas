# Atlas

Sistema personal de conocimiento construido sobre [Claude Code](https://claude.ai/code). Mantiene un wiki interconectado que se puebla, consulta y practica con sesiones de Claude.

## Instalación

```bash
git clone https://github.com/AndresPaladino/atlas.git
cd atlas
bash setup.sh
```

`setup.sh` detecta el OS e instala el CLI de extracción automáticamente (también instalable por separado desde `tools/`).

## Uso

```bash
claude   # abrí Claude Code en la raíz del repo
```

| Comando | Para qué |
|---|---|
| `/ingest [ruta]` | Cargar una fuente (PDF, nota) al wiki |
| `/query <pregunta>` | Consultar el wiki |
| `/practice [tema]` | Sesión Socrática (sin soluciones directas) |
| `/lint` | Auditar consistencia del wiki |

Sin slash command, Atlas elige el modo según contexto.

## Licencia

MIT
