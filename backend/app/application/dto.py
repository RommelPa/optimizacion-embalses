from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearCorridaInput:
    caso_estudio: str
    modo_operacion: str
    fecha_proceso: str
    escenario: str
    origen_datos: str
    observaciones: Optional[str] = None
    archivo_entrada: Optional[str] = None