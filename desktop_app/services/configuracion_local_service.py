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
            dto = self._build_dto(payload)
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

    def _build_dto(self, payload: dict) -> ConfiguracionGlobalInput:
        return ConfiguracionGlobalInput(
            c1=self._parse_float(payload, "c1"),
            c2=self._parse_float(payload, "c2"),
            w=self._parse_float(payload, "w"),
            v_max=self._parse_float(payload, "v_max"),
            n_particles=self._parse_int(payload, "n_particles"),
            max_iter=self._parse_int(payload, "max_iter"),
            rendimiento_ch4=self._parse_float(payload, "rendimiento_ch4"),
            rendimiento_ch6=self._parse_float(payload, "rendimiento_ch6"),
            v_inicio_factor=self._parse_float(payload, "v_inicio_factor"),
            v_final_factor=self._parse_float(payload, "v_final_factor"),
            v_cincel_max=self._parse_float(payload, "v_cincel_max"),
            v_cincel_min=self._parse_float(payload, "v_cincel_min"),
            v_campanario_max=self._parse_float(payload, "v_campanario_max"),
            v_campanario_min=self._parse_float(payload, "v_campanario_min"),
            q_rango_min=self._parse_float(payload, "q_rango_min"),
            q_rango_max=self._parse_float(payload, "q_rango_max"),
        )

    def _parse_float(self, payload: dict, field_name: str) -> float:
        raw_value = str(payload.get(field_name, "")).strip()
        if not raw_value:
            raise ValueError(f"El campo '{field_name}' es obligatorio.")

        try:
            return float(raw_value)
        except ValueError as exc:
            raise ValueError(
                f"El campo '{field_name}' debe ser un número válido."
            ) from exc

    def _parse_int(self, payload: dict, field_name: str) -> int:
        raw_value = str(payload.get(field_name, "")).strip()
        if not raw_value:
            raise ValueError(f"El campo '{field_name}' es obligatorio.")

        try:
            value = float(raw_value)
        except ValueError as exc:
            raise ValueError(
                f"El campo '{field_name}' debe ser un número entero válido."
            ) from exc

        if not value.is_integer():
            raise ValueError(
                f"El campo '{field_name}' debe ser un número entero válido."
            )

        return int(value)