# atlas (CLI)

Backend de Atlas. Dos responsabilidades:

1. **Knowledge graph** (liviano, solo `pyyaml`): valida, audita, indexa el wiki y
   maneja el estado de sesión que enforcea el firewall. No necesita GPU ni torch.
2. **Extracción de PDFs** (pesado, extra `[extract]`): convierte `raw/*.pdf` a
   markdown con LaTeX y captions de figuras usando la GPU (CUDA/MPS/CPU).

## Instalación

```bash
./install.sh        # macOS / Linux  → instala atlas[extract,render]
.\install.ps1       # Windows (PowerShell)
```

Solo necesitás Python. El script instala `uv` si falta y configura el backend de torch automáticamente.

Si solo querés el knowledge tooling (validate/lint/index/session) sin los ~8 GB de
modelos de extracción: `uv tool install .` (sin el extra `[extract]`).

**Captions de figuras (opcional):** requiere [Ollama](https://ollama.com/download) + `ollama pull qwen2.5vl:7b`. Sin esto la extracción funciona igual pero sin describir imágenes.

## Knowledge graph

```bash
atlas validate                 # valida el frontmatter de todas las páginas (exit≠0 si hay errores)
atlas lint [scope] [--json]    # audita el wiki: orphans, links/aristas rotos, simetría, drift
atlas index                    # regenera wiki/index.md y los MOCs desde el filesystem
atlas log [-n N]               # log de mutaciones del wiki, derivado de git
atlas session set "<T>"        # arranca sesión practice sobre T (calcula slugs bloqueados)
atlas session mode <modo>      # cambia modo (query|practice|ingest|lint); cualquier modo ≠ practice levanta el firewall
atlas session reveal | clear   # válvula del firewall / reset
atlas session check <archivo>  # ¿el firewall permite leer? (lo usa el hook PreToolUse)
atlas session show             # muestra modo, tema T y slugs bloqueados actuales
atlas forget <fuente>          # olvida una fuente; preserva entidades compartidas (--dry-run / -y)
atlas ingest-status [--json]   # estado raw→wiki de cada fuente: new/stale/current/missing-raw
atlas ingest-stamp <fuente>    # sella el hash del raw ingerido (lo usa /ingest --compile)
```

`forget` quita el link de la fuente en cada página y borra solo las que quedan
sin ninguna fuente (las que tienen otra sobreviven). `ingest-stamp` graba
`ingested_sha256` en el frontmatter de la fuente; `ingest-status` compara ese hash
con el raw actual para que `--compile` saltee lo que no cambió.

## Servidor MCP

El mismo grafo del wiki se expone como un servidor [MCP](https://modelcontextprotocol.io/)
para cualquier cliente (Claude Desktop, plugins, otro LLM) — desacople del runtime
de Claude Code. Instalar con el extra y correr por stdio:

```bash
uv tool install '.[mcp]'        # o: pip install 'atlas[mcp]'
ATLAS_ROOT=/ruta/al/repo atlas-mcp
```

Tools de lectura: `atlas_query_index`, `atlas_read_page`, `atlas_search`,
`atlas_lint`, `atlas_validate`, `atlas_ingest_status`.
Tools de escritura: `atlas_write_page`, `atlas_index`, `atlas_forget`.
Control de sesión: `atlas_session_set/mode/reveal/clear/show`.
El **firewall de `/practice` se enforça en el server**: `atlas_read_page` consulta
el estado de sesión y deniega las páginas bloqueadas, así que ningún cliente lo puede saltar.

**Claude Desktop** — editar `claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/`; Linux: `~/.config/Claude/`):

```json
{
  "mcpServers": {
    "atlas": {
      "command": "atlas-mcp",
      "env": { "ATLAS_ROOT": "/ruta/al/repo" }
    }
  }
}
```

`setup.sh` configura esto automáticamente si Claude Desktop está instalado.

**Codex CLI** — agregar en `~/.codex/config.yaml` (o `codex.yaml` en la raíz del proyecto):

```yaml
mcp_servers:
  - name: atlas
    command: atlas-mcp
    env:
      ATLAS_ROOT: /ruta/al/repo
```

> El path y formato exacto de Codex puede variar — verificar contra la versión instalada.

## Uso

```bash
atlas doctor                   # hardware detectado y captions disponibles
atlas status                   # PDFs pendientes / convertidos / desactualizados
atlas extract                  # convierte todos los PDFs pendientes de raw/
atlas extract raw/foo.pdf      # un PDF puntual
atlas extract --captions       # + describe figuras (necesita Ollama)
atlas extract --force          # re-extrae todo
atlas extract --no-segment     # no segmentar aunque el doc sea grande
atlas extract --chunk-tokens 4000  # tamaño objetivo de cada chunk (default 3000)
```

## Segmentación de docs grandes

Un libro de cientos de páginas extrae a un markdown gigante que Claude no puede procesar de una sola lectura. Por eso, para docs grandes (**≥40 páginas** o **≥25k tokens** estimados), `atlas extract` produce además un índice + chunks, y `/ingest` lee el índice primero y solo los chunks que necesita.

Para `raw/Notas.pdf` se generan:

```
raw/Notas.md            # monolítico (se sigue escribiendo siempre; fallback y render)
raw/Notas.toc.md        # índice: árbol de headings + páginas + tokens estimados + chunk que lo contiene
raw/Notas/              # chunks por sección (.md), nunca cortando un tema a la mitad
  00-introduccion.md
  01-preliminares.md
  ...
```

- Cada chunk arranca con un breadcrumb (fuente, rango de páginas, ruta de headings) para ser legible en aislamiento.
- Los docs chicos (exámenes, papers cortos) no se segmentan: queda solo el `.md`, como antes.
- El TOC y los chunks **se versionan en git** (igual que el `.md` y el manifest): se extrae en una máquina y se hace `pull` en otra sin re-extraer. Las imágenes siguen siendo locales.
- Flags: `--segment` fuerza la segmentación, `--no-segment` la inhibe, `--chunk-tokens N` ajusta el tamaño objetivo.

La página `wiki/sources/<slug>.md` deriva su "Mapa de coverage" directo del TOC, así que el grafo apunta a las secciones exactas sin recargar el documento entero.
