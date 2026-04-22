from __future__ import annotations

from app.application.configuracion_service import ConfiguracionService
from app.application.dto import ConfiguracionGlobalInput
from app.db.session import SessionLocal


class ConfiguracionLocalService:
    def obtener_configuracion(self) -> dict:
        db = SessionLocal()
        try:
            service = ConfiguracionService(db)
            return service.obtener_configuracion()
        finally:
            db.close()

    def guardar_configuracion(self, payload: dict) -> dict:
        db = SessionLocal()
        try:
            service = ConfiguracionService(db)

            dto = ConfiguracionGlobalInput(
                c1=float(payload["c1"]),
                c2=float(payload["c2"]),
                w=float(payload["w"]),
                v_max=float(payload["v_max"]),
                n_particles=int(payload["n_particles"]),
                max_iter=int(payload["max_iter"]),
                rendimiento_ch4=float(payload["rendimiento_ch4"]),
                rendimiento_ch6=float(payload["rendimiento_ch6"]),
                v_inicio_factor=float(payload["v_inicio_factor"]),
                v_final_factor=float(payload["v_final_factor"]),
                v_cincel_max=float(payload["v_cincel_max"]),
                v_cincel_min=float(payload["v_cincel_min"]),
                v_campanario_max=float(payload["v_campanario_max"]),
                v_campanario_min=float(payload["v_campanario_min"]),
                q_rango_min=float(payload["q_rango_min"]),
                q_rango_max=float(payload["q_rango_max"]),
            )

            return service.guardar_configuracion(dto)
        finally:
            db.close()

    def restaurar_configuracion_por_defecto(self) -> dict:
        db = SessionLocal()
        try:
            service = ConfiguracionService(db)
            return service.restaurar_configuracion_por_defecto()
        finally:
            db.close()