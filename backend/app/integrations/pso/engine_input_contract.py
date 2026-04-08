from typing import Literal

from pydantic import BaseModel, Field, field_validator


class SeriesInput(BaseModel):
    q_cincel: list[float]
    costo_marginal: list[float]

    @field_validator("q_cincel", "costo_marginal")
    @classmethod
    def validar_series_no_vacias(cls, value: list[float]) -> list[float]:
        if not value:
            raise ValueError("La serie no puede estar vacia")
        return value


class RestriccionesInput(BaseModel):
    q_salida_campanario: float

    v_cincel_inicio: float
    v_campanario_inicio: float
    v_cincel_final: float
    v_campanario_final: float

    v_cincel_max: float
    v_cincel_min: float
    v_campanario_max: float
    v_campanario_min: float

    q_rango_min: float = 6.0
    q_rango_max: float = 15.0

    rendimiento_ch4: float = 1.01
    rendimiento_ch6: float = 0.59


class ConfiguracionPSOInput(BaseModel):
    n_particles: int = Field(default=10, ge=1)
    max_iter: int = Field(default=5, ge=1)


class EngineInputContract(BaseModel):
    modo_operacion: Literal["inicial", "reprograma"]
    fecha_proceso: str
    origen_datos: Literal["manual", "csv", "excel"]

    series: SeriesInput
    restricciones: RestriccionesInput
    configuracion_pso: ConfiguracionPSOInput

    @property
    def horas(self) -> int:
        return len(self.series.q_cincel)

    @field_validator("fecha_proceso")
    @classmethod
    def validar_fecha_no_vacia(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("fecha_proceso no puede estar vacia")
        return value

    @field_validator("configuracion_pso")
    @classmethod
    def validar_configuracion(cls, value: ConfiguracionPSOInput) -> ConfiguracionPSOInput:
        return value

    @field_validator("series")
    @classmethod
    def validar_longitudes_series(cls, value: SeriesInput) -> SeriesInput:
        if len(value.q_cincel) != len(value.costo_marginal):
            raise ValueError("q_cincel y costo_marginal deben tener la misma longitud")
        return value