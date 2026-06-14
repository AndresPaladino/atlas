"""atlas-local · wiki — backend determinístico del knowledge graph.

Este sub-paquete es la columna vertebral de código de Atlas: parsea el wiki,
valida el contrato de frontmatter, corre los checks de consistencia (lint),
regenera el índice y los MOCs, y mantiene el estado de sesión que enforcea el
firewall del modo `/practice`.

Es **liviano**: depende solo de ``pyyaml`` (parseo de frontmatter), no de
``torch``/``marker``. La extracción de PDFs (pesada, GPU) vive aparte en
``atlas_local.extract`` y se importa de forma perezosa. Así ``atlas lint`` no
exige instalar 8 GB de modelos.
"""

from __future__ import annotations
