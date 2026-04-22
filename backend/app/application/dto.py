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

@dataclass
class ConfiguracionGlobalInput:
    c1: float
    c2: float
    w: float
    v_max: float
    n_particles: int
    max_iter: int

    rendimiento_ch4: float
    rendimiento_ch6: float
    v_inicio_factor: float
    v_final_factor: float

    v_cincel_max: float
    v_cincel_min: float
    v_campanario_max: float
    v_campanario_min: float
    q_rango_min: float
    q_rango_max: float