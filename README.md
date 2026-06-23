# Atlas

[![CI](https://github.com/AndresPaladino/atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/AndresPaladino/atlas/actions/workflows/ci.yml)
[![Python ≥3.10](https://img.shields.io/badge/python-%E2%89%A53.10-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema personal de conocimiento construido sobre [Claude Code](https://claude.ai/code). Mantiene un wiki interconectado que se popula, consulta y practica con sesiones de Claude. Incluye un CLI (`atlas`) para extracción de PDFs y mantenimiento del grafo.

```mermaid
flowchart LR
    U((vos))

    subgraph raw["raw/"]
        PDFs["PDFs · apuntes"]
    end

    subgraph extracted["extracted/"]
        MD["markdown + figuras"]
    end

    subgraph wiki["wiki/ — grafo de conocimiento"]
        S["sources/"]
        C["concepts · theorems · methods"]
    end

    subgraph claude["Claude Code"]
        I["/ingest — poblar"]
        Q["/query — consultar"]
        P["/practice — Socrático 🔒"]
    end

    subgraph maint["atlas CLI — mantenimiento"]
        M["validate · lint · index"]
    end

    U -->|"subís un PDF"| raw
    raw -->|"atlas extract"| extracted
    extracted -->|"/ingest"| S
    S --> C
    C -->|"lee"| Q
    C -.->|"firewall (no spoilers)"| P
    U -->|"tenés una duda"| Q
    U -->|"querés practicar"| P
    wiki <-->|"audita / regenera"| maint
```

## Requisitos

- **Python ≥3.10** — para el CLI `atlas`.
- **[Claude Code](https://claude.ai/code)** — requerido para los modos `/ingest`, `/query` y `/practice`. El CLI por sí solo extrae PDFs y mantiene el grafo, pero el valor central (poblar/consultar/practicar) vive en sesiones de Claude.
- **GPU + ~8 GB de modelos** — requeridos solo para `atlas extract` con calidad (marker). Sin GPU, `atlas extract` cae a un fallback de texto plano (markitdown); el resto del CLI no necesita nada de esto. Ver [`tools/README.md`](tools/README.md).

## Instalación

```bash
git clone https://github.com/AndresPaladino/atlas.git
cd atlas
bash setup.sh
```

`setup.sh` crea la estructura del wiki, el directorio `extracted/` (donde `atlas extract` escribe los markdown + figuras) e instala el CLI `atlas`.

Para navegar el wiki en Obsidian, abrí la carpeta `wiki/` como vault (no la raíz del repo).

## Verificá la instalación

```bash
atlas doctor   # device, torch, tier de extracción y disponibilidad de captions
atlas status   # PDFs pendientes / convertidos en raw/
```

`atlas doctor` no descarga modelos: imprime el diagnóstico del entorno (GPU/CPU, si torch está disponible, qué extractor usará). Si corre sin error, el CLI quedó bien instalado.

## Uso

```bash
claude   # abrir Claude Code en la raíz del repositorio
```

| Comando | Para qué |
|---|---|
| `/ingest [ruta]` | Cargar una fuente (PDF, nota) al wiki |
| `/query <pregunta>` | Consultar el wiki |
| `/practice [tema]` | Sesión Socrática (sin soluciones directas) |
| `/lint` | Auditar consistencia del wiki |

Sin slash command, Atlas elige el modo según contexto.

## CLI `atlas`

```bash
# Knowledge graph
atlas validate        # valida frontmatter del wiki
atlas lint            # audita orphans, links rotos, drift
atlas index           # regenera index.md y MOCs

# Extracción de PDFs (raw/ → extracted/)
atlas extract         # convierte PDFs de raw/ a markdown en extracted/
atlas status          # PDFs pendientes / convertidos / desactualizados
```

Ver `tools/README.md` para opciones completas (segmentación, captions con Ollama, etc.).

## Licencia

MIT
