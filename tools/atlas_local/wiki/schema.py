"""El contrato de frontmatter del wiki, como código.

Única fuente de verdad de lo que ``schema/wiki-conventions.md`` describe en
prosa. ``validate`` y ``lint`` consumen estas reglas; el documento de schema
referencia este módulo como autoridad.

Mantenido como datos + funciones puras (sin pydantic) para no sumar una
dependencia: el resto del paquete ya usa dataclasses y validación manual.
"""

from __future__ import annotations

from .loader import Page

# Tipos válidos de página (una página tiene exactamente uno). Coincide con las
# carpetas bajo wiki/ salvo index/log/README, que no son páginas de contenido.
VALID_TYPES = frozenset(
    {
        "concept", "theorem", "method", "example", "comparison",
        "source", "assessment", "area",
    }
)

# Áreas con MOC propio, en orden canónico (lo usa `atlas index` para listar los
# MOCs). Las páginas pueden declarar otras, pero entonces no aparecen en ningún
# MOC → validate lo marca como warning (no error). Única fuente de verdad: el
# resto del paquete (p.ej. index.py) importa de acá, sin redefinir la lista.
AREAS_ORDERED = ("math", "signals", "computing", "engineering-physics", "ml")
KNOWN_AREAS = frozenset(AREAS_ORDERED)

# Campos obligatorios para todo tipo excepto `area` (los MOC son livianos).
_REQUIRED_COMMON = ("type", "title", "areas", "created", "updated")

# Campos extra obligatorios por tipo.
_REQUIRED_BY_TYPE: dict[str, tuple[str, ...]] = {
    "theorem": ("statement_form",),
    "method": ("when_to_use", "fails_when"),
    "example": ("illustrates", "difficulty"),
    "comparison": ("compares",),
    "source": ("source_kind", "path"),
    "assessment": ("assessment_kind", "path"),
    "area": ("tag_prefix",),
}

# Carpeta esperada por tipo (para detectar archivos en la carpeta equivocada).
FOLDER_BY_TYPE: dict[str, str] = {
    "concept": "concepts",
    "theorem": "theorems",
    "method": "methods",
    "example": "examples",
    "comparison": "comparisons",
    "source": "sources",
    "assessment": "assessments",
    "area": "areas",
}

_VALID_SOURCE_KINDS = frozenset({"book", "paper", "notes", "lecture"})
_VALID_ASSESSMENT_KINDS = frozenset({"exam", "parcial", "practica"})


def required_fields(page_type: str | None) -> tuple[str, ...]:
    """Campos obligatorios para un tipo dado (comunes + específicos)."""
    if page_type == "area":
        base: tuple[str, ...] = ("type", "title", "updated")
    else:
        base = _REQUIRED_COMMON
    return base + _REQUIRED_BY_TYPE.get(page_type or "", ())


def validate_page(page: Page) -> list[str]:
    """Lista de errores de schema de una página. Vacía = válida.

    Errores (rompen el contrato). Las observaciones blandas (área desconocida)
    se devuelven con prefijo ``warn:`` para que el llamador las separe.
    """
    errors: list[str] = []

    if page.fm_error:
        return [f"frontmatter ilegible: {page.fm_error}"]

    ptype = page.type
    if ptype is None:
        errors.append("falta 'type'")
    elif ptype not in VALID_TYPES:
        errors.append(f"'type' inválido: {ptype!r} (válidos: {sorted(VALID_TYPES)})")

    # Campos obligatorios.
    for fld in required_fields(ptype):
        val = page.frontmatter.get(fld)
        if val is None or (isinstance(val, (list, str)) and len(val) == 0):
            errors.append(f"falta campo obligatorio '{fld}'")

    # Carpeta coherente con el tipo.
    if ptype in FOLDER_BY_TYPE and page.folder != FOLDER_BY_TYPE[ptype]:
        errors.append(
            f"tipo '{ptype}' debería vivir en '{FOLDER_BY_TYPE[ptype]}/', "
            f"está en '{page.folder}/'"
        )

    # Validaciones específicas.
    if ptype == "source":
        kind = page.frontmatter.get("source_kind")
        if kind is not None and kind not in _VALID_SOURCE_KINDS:
            errors.append(
                f"source_kind inválido: {kind!r} (válidos: {sorted(_VALID_SOURCE_KINDS)})"
            )
    if ptype == "assessment":
        kind = page.frontmatter.get("assessment_kind")
        if kind is not None and kind not in _VALID_ASSESSMENT_KINDS:
            errors.append(
                f"assessment_kind inválido: {kind!r} "
                f"(válidos: {sorted(_VALID_ASSESSMENT_KINDS)})"
            )
    if ptype == "example":
        diff = page.frontmatter.get("difficulty")
        if diff is not None and diff not in (1, 2, 3):
            errors.append(f"difficulty debe ser 1, 2 o 3 (es {diff!r})")

    # Áreas desconocidas → warning (no aparecerán en ningún MOC).
    for area in page.areas:
        if area not in KNOWN_AREAS:
            errors.append(f"warn: área desconocida '{area}' (no tiene MOC)")

    return errors
