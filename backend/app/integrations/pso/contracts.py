from typing import Optional

from pydantic import BaseModel


class PSOWrapperInput(BaseModel):
    corrida_id: str
    modo_operacion: str
    fecha_proceso: str
    escenario: str
    origen_datos: str
    observaciones: Optional[str] = None
    archivo_entrada: Optional[str] = None


class PSOWrapperOutput(BaseModel):
    estado: str
    version_modelo: str
    modo_ejecucion: str
    mensaje_modelo: str
    best_cost: float
    execution_time_sec: float
    q_opt: list[float]
    v_cincel: list[float]
    v_campanario: list[float]
    cmg: list[float]
    potencia_ch4: list[float]
    potencia_ch6: list[float]
    ingreso: list[float]
    q_salida_campanario: float
    p_char_5: list[float]