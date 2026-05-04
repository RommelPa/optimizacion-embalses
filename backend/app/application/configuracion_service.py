from sqlalchemy.orm import Session

from app.application.dto import ConfiguracionGlobalInput
from app.models.configuracion_global import ConfiguracionGlobal
from app.repositories.configuracion_global_repository import (
    ConfiguracionGlobalRepository,
)


class ConfiguracionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = ConfiguracionGlobalRepository(db)

    def obtener_configuracion(self) -> dict:
        row = self.repo.ensure_exists()
        return self._to_dict(row)

    def guardar_configuracion(self, payload: ConfiguracionGlobalInput) -> dict:
        self._validar(payload)

        row = self.repo.ensure_exists()

        row.c1 = payload.c1
        row.c2 = payload.c2
        row.w = payload.w
        row.v_max = payload.v_max
        row.n_particles = payload.n_particles
        row.max_iter = payload.max_iter

        row.rendimiento_ch4 = payload.rendimiento_ch4
        row.rendimiento_ch6 = payload.rendimiento_ch6
        row.v_inicio_factor = payload.v_inicio_factor
        row.v_final_factor = payload.v_final_factor

        row.v_cincel_max = payload.v_cincel_max
        row.v_cincel_min = payload.v_cincel_min
        row.v_campanario_max = payload.v_campanario_max
        row.v_campanario_min = payload.v_campanario_min
        row.q_rango_min = payload.q_rango_min
        row.q_rango_max = payload.q_rango_max

        row = self.repo.save(row)
        return self._to_dict(row)

    def restaurar_configuracion_por_defecto(self) -> dict:
        row = self.repo.ensure_exists()
        defaults = self._default_values()

        row.c1 = defaults["c1"]
        row.c2 = defaults["c2"]
        row.w = defaults["w"]
        row.v_max = defaults["v_max"]
        row.n_particles = defaults["n_particles"]
        row.max_iter = defaults["max_iter"]

        row.rendimiento_ch4 = defaults["rendimiento_ch4"]
        row.rendimiento_ch6 = defaults["rendimiento_ch6"]
        row.v_inicio_factor = defaults["v_inicio_factor"]
        row.v_final_factor = defaults["v_final_factor"]

        row.v_cincel_max = defaults["v_cincel_max"]
        row.v_cincel_min = defaults["v_cincel_min"]
        row.v_campanario_max = defaults["v_campanario_max"]
        row.v_campanario_min = defaults["v_campanario_min"]
        row.q_rango_min = defaults["q_rango_min"]
        row.q_rango_max = defaults["q_rango_max"]

        row = self.repo.save(row)
        return self._to_dict(row)

    def _validar(self, payload: ConfiguracionGlobalInput) -> None:
        if payload.c1 <= 0:
            raise ValueError("c1 debe ser mayor que 0")

        if payload.c2 <= 0:
            raise ValueError("c2 debe ser mayor que 0")

        if payload.w <= 0:
            raise ValueError("w debe ser mayor que 0")

        if payload.v_max <= 0:
            raise ValueError("v_max debe ser mayor que 0")

        if payload.n_particles < 1:
            raise ValueError("n_particles debe ser mayor o igual a 1")

        if payload.max_iter < 1:
            raise ValueError("max_iter debe ser mayor o igual a 1")

        if payload.rendimiento_ch4 <= 0:
            raise ValueError("rendimiento_ch4 debe ser mayor que 0")

        if payload.rendimiento_ch6 <= 0:
            raise ValueError("rendimiento_ch6 debe ser mayor que 0")

        if payload.v_inicio_factor <= 0:
            raise ValueError("v_inicio_factor debe ser mayor que 0")

        if payload.v_final_factor <= 0:
            raise ValueError("v_final_factor debe ser mayor que 0")

        if payload.v_cincel_min >= payload.v_cincel_max:
            raise ValueError("v_cincel_min debe ser menor que v_cincel_max")

        if payload.v_campanario_min >= payload.v_campanario_max:
            raise ValueError("v_campanario_min debe ser menor que v_campanario_max")

        if payload.q_rango_min >= payload.q_rango_max:
            raise ValueError("q_rango_min debe ser menor que q_rango_max")

    def _to_dict(self, row: ConfiguracionGlobal) -> dict:
        return {
            "id": row.id,
            "c1": row.c1,
            "c2": row.c2,
            "w": row.w,
            "v_max": row.v_max,
            "n_particles": row.n_particles,
            "max_iter": row.max_iter,
            "rendimiento_ch4": row.rendimiento_ch4,
            "rendimiento_ch6": row.rendimiento_ch6,
            "v_inicio_factor": row.v_inicio_factor,
            "v_final_factor": row.v_final_factor,
            "v_cincel_max": row.v_cincel_max,
            "v_cincel_min": row.v_cincel_min,
            "v_campanario_max": row.v_campanario_max,
            "v_campanario_min": row.v_campanario_min,
            "q_rango_min": row.q_rango_min,
            "q_rango_max": row.q_rango_max,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }

    def _default_values(self) -> dict:
        return {
            "c1": 2.0,
            "c2": 2.0,
            "w": 0.9,
            "v_max": 1.5,
            "n_particles": 150,
            "max_iter": 150,
            "rendimiento_ch4": 1.01,
            "rendimiento_ch6": 0.59,
            "v_inicio_factor": 0.85,
            "v_final_factor": 0.85,
            "v_cincel_max": 190000.0,
            "v_cincel_min": 20000.0,
            "v_campanario_max": 90000.0,
            "v_campanario_min": 20000.0,
            "q_rango_min": 6.0,
            "q_rango_max": 15.0,
        }