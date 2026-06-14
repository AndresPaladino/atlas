# atlas bootstrap (Windows / PowerShell)
# Uso:  cd atlas\tools ;  .\install.ps1
#
# Instala el comando global `atlas` via uv tool.
# Idempotente: instala uv si falta, luego instala/reinstala atlas.

$ErrorActionPreference = "Stop"

function Say  ($m) { Write-Host "▸ $m" -ForegroundColor Cyan }
function Warn ($m) { Write-Host "⚠ $m" -ForegroundColor Yellow }
function Ok   ($m) { Write-Host "✓ $m" -ForegroundColor Green }

# ── 1. uv ────────────────────────────────────────────────────────────────────
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Say "uv no encontrado; instalando (instalador oficial de Astral)…"
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Warn "uv sigue sin estar en PATH. Abrí una PowerShell nueva y reintentá."
    exit 1
}
Ok "uv $((uv --version).Split(' ')[1])"

# ── 2. Instalar atlas globalmente ─────────────────────────────────────────────
Say "Instalando atlas como comando global (uv tool install)…"
$env:UV_TORCH_BACKEND = "auto"
uv tool install "${PSScriptRoot}[extract,render]"
Ok "atlas instalado en PATH"

# ── 3. Ollama (opcional, solo para captions de figuras) ──────────────────────
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Ok "Ollama detectado — captions de figuras disponibles (--captions)."
} else {
    Warn "Ollama no instalado. La extracción funciona igual; los captions de figuras"
    Warn "quedan deshabilitados. Para habilitarlos: https://ollama.com/download"
    Warn "y luego:  ollama pull qwen2.5vl:7b"
}

# ── 4. Doctor ─────────────────────────────────────────────────────────────────
Say "Diagnóstico de hardware:"
atlas doctor

Write-Host ""
Ok "Instalación completa. Probá desde cualquier directorio:  atlas status"
