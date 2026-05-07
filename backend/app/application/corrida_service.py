from __future__ import annotations

import json
from uuid import uuid4

import numpy as np
from sqlalchemy.orm import Session

from app.application.authorization import require_ingeniero
from app.application.configuracion_service import ConfiguracionService
from app.application.corrida_resultados_builder import build_resultados_dataset
from app.application.dto import CrearCorridaInput, CrearCorridaManualInput
from app.application.errors import (
    CorridaExecutionAppError,
    CorridaNotFoundError,
    CorridaValidationAppError,
)
from app.application.excel_exporter import build_excel_corrida_legacy
from app.application.utils import serialize_datetime_utc
from app.integrations.pso.contracts import PSOWrapperInput, PSOWrapperOutput
from app.integrations.pso.engine.engine_runner import run_pso_engine
from app.integrations.pso.engine_input_contract import EngineInputContract
from app.integrations.pso.errors import PSOExecutionError, PSOValidationError
from app.integrations.pso.manual_input_builder import build_engine_input_from_manual
from app.integrations.pso.wrapper import ejecutar_corrida_pso
from app.models.corrida import Corrida
from app.repositories.corrida_repository import CorridaRepository


class CorridaService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = CorridaRepository(db)

    def crear_corrida(self, payload: CrearCorridaInput) -> dict:
        corrida_id = str(uuid4())
        input_payload_json = json.dumps(payload.__dict__)
        config_actual = self._obtener_configuracion_actual()

        wrapper_input = PSOWrapperInput(
            corrida_id=corrida_id,
            modo_operacion=payload.modo_operacion,
            fecha_proceso=payload.fecha_proceso,
            escenario=payload.escenario,
            origen_datos=payload.origen_datos,
            observaciones=payload.observaciones,
            archivo_entrada=payload.archivo_entrada,
        )

        try:
            wrapper_result = ejecutar_corrida_pso(wrapper_input)
            self._persistir_corrida_exitosa(
                corrida_id=corrida_id,
                payload=payload,
                input_payload_json=input_payload_json,
                config_actual=config_actual,
                wrapper_result=wrapper_result,
            )
            return self._build_success_response(
                corrida_id=corrida_id,
                payload=payload,
                wrapper_result=wrapper_result,
            )

        except PSOValidationError as exc:
            self._persistir_corrida_error(
                corrida_id=corrida_id,
                payload=payload,
                input_payload_json=input_payload_json,
                config_actual=config_actual,
                estado="rechazada",
                modo_ejecucion="error_validacion",
                mensaje_modelo="La corrida fue rechazada por error de validación de entrada",
                error_message=str(exc),
            )
            raise CorridaValidationAppError(str(exc)) from exc

        except PSOExecutionError as exc:
            self._persistir_corrida_error(
                corrida_id=corrida_id,
                payload=payload,
                input_payload_json=input_payload_json,
                config_actual=config_actual,
                estado="fallida",
                modo_ejecucion="error_ejecucion",
                mensaje_modelo="La corrida falló durante la ejecución del motor",
                error_message=str(exc),
            )
            raise CorridaExecutionAppError(str(exc)) from exc

    def crear_corrida_manual(self, payload: CrearCorridaManualInput) -> dict:
        corrida_id = str(uuid4())
        input_payload_json = self._build_manual_input_payload_json(payload)
        config_actual = self._obtener_configuracion_actual()

        if payload.corrida_base_id:
            corrida_base = self.repo.get_by_id(payload.corrida_base_id)
            if corrida_base is None:
                raise CorridaValidationAppError("La corrida base indicada no existe.")

        try:
            engine_input = build_engine_input_from_manual(
                q_salida_campanario=payload.q_salida_campanario,
                cmg=payload.cmg,
                p_char_5=payload.p_char_5,
                configuracion=config_actual,
                modo_operacion=payload.modo_operacion,
                fecha_proceso=payload.fecha_proceso,
                origen_datos=payload.origen_datos,
            )
            wrapper_result = self._ejecutar_engine_input(
                engine_input=engine_input,
                escenario=payload.escenario,
                origen_datos=payload.origen_datos,
            )
            self._persistir_corrida_exitosa(
                corrida_id=corrida_id,
                payload=payload,
                input_payload_json=input_payload_json,
                config_actual=config_actual,
                wrapper_result=wrapper_result,
            )
            return self._build_success_response(
                corrida_id=corrida_id,
                payload=payload,
                wrapper_result=wrapper_result,
            )

        except PSOValidationError as exc:
            self._persistir_corrida_error(
                corrida_id=corrida_id,
                payload=payload,
                input_payload_json=input_payload_json,
                config_actual=config_actual,
                estado="rechazada",
                modo_ejecucion="error_validacion",
                mensaje_modelo="La corrida manual fue rechazada por error de validación de entrada",
                error_message=str(exc),
            )
            raise CorridaValidationAppError(str(exc)) from exc

        except PSOExecutionError as exc:
            self._persistir_corrida_error(
                corrida_id=corrida_id,
                payload=payload,
                input_payload_json=input_payload_json,
                config_actual=config_actual,
                estado="fallida",
                modo_ejecucion="error_ejecucion",
                mensaje_modelo="La corrida manual falló durante la ejecución del motor",
                error_message=str(exc),
            )
            raise CorridaExecutionAppError(str(exc)) from exc

    def listar_corridas(
        self,
        origen_datos: str | None = None,
        estado: str | None = None,
        id_contains: str | None = None,
        fecha_proceso: str | None = None,
    ) -> dict:
        rows = self.repo.list_filtered(
            origen_datos=origen_datos,
            estado=estado,
            id_contains=id_contains,
            fecha_proceso=fecha_proceso,
        )

        items = [
            {
                "id": row.id,
                "caso_estudio": row.caso_estudio,
                "created_at": serialize_datetime_utc(row.created_at),
                "fecha_proceso": row.fecha_proceso,
                "modo_operacion": row.modo_operacion,
                "escenario": row.escenario,
                "origen_datos": row.origen_datos,
                "estado": row.estado,
                "version_modelo": row.version_modelo,
                "modo_ejecucion": row.modo_ejecucion,
                "best_cost": row.best_cost,
                "execution_time_sec": row.execution_time_sec,
                "usuario_username": row.usuario_username,
                "usuario_rol": row.usuario_rol,
                "es_caso_base": row.es_caso_base,
                "corrida_base_id": row.corrida_base_id,
            }
            for row in rows
        ]

        return {
            "items": items,
            "total": len(items),
        }

    def obtener_corrida(self, corrida_id: str) -> dict:
        row = self.repo.get_by_id(corrida_id)

        if not row:
            raise CorridaNotFoundError("Corrida no encontrada")

        resultados_dataset = build_resultados_dataset(row)

        return {
            "id": row.id,
            "caso_estudio": row.caso_estudio,
            "created_at": serialize_datetime_utc(row.created_at),
            "fecha_proceso": row.fecha_proceso,
            "modo_operacion": row.modo_operacion,
            "escenario": row.escenario,
            "origen_datos": row.origen_datos,
            "observaciones": row.observaciones,
            "estado": row.estado,
            "version_modelo": row.version_modelo,
            "modo_ejecucion": row.modo_ejecucion,
            "mensaje_modelo": row.mensaje_modelo,
            "best_cost": row.best_cost,
            "execution_time_sec": row.execution_time_sec,
            "q_salida_campanario": row.q_salida_campanario,
            "q_opt": json.loads(row.q_opt_json),
            "v_cincel": json.loads(row.v_cincel_json),
            "v_campanario": json.loads(row.v_campanario_json),
            "cmg": json.loads(row.cmg_json),
            "potencia_ch4": json.loads(row.potencia_ch4_json),
            "potencia_ch6": json.loads(row.potencia_ch6_json),
            "ingreso": json.loads(row.ingreso_json),
            "p_char_5": json.loads(row.p_char_5_json),
            "input_payload_json": row.input_payload_json,
            "error_message": row.error_message,
            "usuario_id": row.usuario_id,
            "usuario_username": row.usuario_username,
            "usuario_rol": row.usuario_rol,
            "es_caso_base": row.es_caso_base,
            "corrida_base_id": row.corrida_base_id,
            "configuracion_usada": self._build_configuracion_usada_dict(row),
            "resultados_dataset": resultados_dataset,
        }

    def obtener_caso_base(self) -> dict | None:
        row = self.repo.get_current_caso_base()
        if row is None:
            return None

        return {
            "id": row.id,
            "caso_estudio": row.caso_estudio,
            "created_at": serialize_datetime_utc(row.created_at),
            "fecha_proceso": row.fecha_proceso,
            "modo_operacion": row.modo_operacion,
            "escenario": row.escenario,
            "origen_datos": row.origen_datos,
            "observaciones": row.observaciones,
            "estado": row.estado,
            "q_salida_campanario": row.q_salida_campanario,
            "cmg": json.loads(row.cmg_json),
            "p_char_5": json.loads(row.p_char_5_json),
            "input_payload_json": row.input_payload_json,
            "es_caso_base": row.es_caso_base,
        }

    def marcar_como_caso_base(self, corrida_id: str, user_session) -> None:
        require_ingeniero(user_session)

        row = self.repo.get_by_id(corrida_id)
        if not row:
            raise CorridaNotFoundError("Corrida no encontrada")

        if row.estado != "completada":
            raise ValueError("Solo una corrida completada puede marcarse como caso base.")

        self.repo.mark_as_caso_base(row)

    def exportar_corrida_excel(self, corrida_id: str) -> tuple[bytes, str]:
        row = self.repo.get_by_id(corrida_id)

        if not row:
            raise CorridaNotFoundError("Corrida no encontrada")

        return build_excel_corrida_legacy(row)

    def _obtener_configuracion_actual(self) -> dict:
        config_service = ConfiguracionService(self.db)
        return config_service.obtener_configuracion()

    def _persistir_corrida_exitosa(
        self,
        *,
        corrida_id: str,
        payload,
        input_payload_json: str,
        config_actual: dict,
        wrapper_result: PSOWrapperOutput,
    ) -> None:
        corrida_db = Corrida(
            **self._build_corrida_base_fields(
                corrida_id=corrida_id,
                payload=payload,
                input_payload_json=input_payload_json,
                config_actual=config_actual,
            ),
            **self._build_corrida_success_fields(wrapper_result),
        )
        self.repo.add(corrida_db)

    def _persistir_corrida_error(
        self,
        *,
        corrida_id: str,
        payload,
        input_payload_json: str,
        config_actual: dict,
        estado: str,
        modo_ejecucion: str,
        mensaje_modelo: str,
        error_message: str,
    ) -> None:
        corrida_db = Corrida(
            **self._build_corrida_base_fields(
                corrida_id=corrida_id,
                payload=payload,
                input_payload_json=input_payload_json,
                config_actual=config_actual,
            ),
            **self._build_corrida_error_fields(
                estado=estado,
                modo_ejecucion=modo_ejecucion,
                mensaje_modelo=mensaje_modelo,
                error_message=error_message,
            ),
        )
        self.repo.add(corrida_db)

    def _build_corrida_base_fields(
        self,
        corrida_id: str,
        payload,
        input_payload_json: str,
        config_actual: dict,
    ) -> dict:
        return {
            "id": corrida_id,
            "caso_estudio": payload.caso_estudio,
            "fecha_proceso": payload.fecha_proceso,
            "modo_operacion": payload.modo_operacion,
            "escenario": payload.escenario,
            "origen_datos": payload.origen_datos,
            "observaciones": payload.observaciones,
            "input_payload_json": input_payload_json,
            "es_caso_base": False,
            "corrida_base_id": getattr(payload, "corrida_base_id", None),
            **self._build_config_snapshot_fields(config_actual),
            **self._build_user_audit_fields(payload),
        }

    def _build_corrida_success_fields(self, wrapper_result: PSOWrapperOutput) -> dict:
        return {
            "estado": "completada",
            "version_modelo": wrapper_result.version_modelo,
            "modo_ejecucion": wrapper_result.modo_ejecucion,
            "mensaje_modelo": wrapper_result.mensaje_modelo,
            "best_cost": wrapper_result.best_cost,
            "execution_time_sec": wrapper_result.execution_time_sec,
            "q_salida_campanario": wrapper_result.q_salida_campanario,
            "q_opt_json": json.dumps(wrapper_result.q_opt),
            "v_cincel_json": json.dumps(wrapper_result.v_cincel),
            "v_campanario_json": json.dumps(wrapper_result.v_campanario),
            "cmg_json": json.dumps(wrapper_result.cmg),
            "potencia_ch4_json": json.dumps(wrapper_result.potencia_ch4),
            "potencia_ch6_json": json.dumps(wrapper_result.potencia_ch6),
            "ingreso_json": json.dumps(wrapper_result.ingreso),
            "p_char_5_json": json.dumps(wrapper_result.p_char_5),
            "error_message": None,
        }

    def _build_corrida_error_fields(
        self,
        estado: str,
        modo_ejecucion: str,
        mensaje_modelo: str,
        error_message: str,
    ) -> dict:
        return {
            "estado": estado,
            "version_modelo": "pso-engine-v1",
            "modo_ejecucion": modo_ejecucion,
            "mensaje_modelo": mensaje_modelo,
            "best_cost": 0.0,
            "execution_time_sec": 0.0,
            "q_salida_campanario": 0.0,
            "q_opt_json": "[]",
            "v_cincel_json": "[]",
            "v_campanario_json": "[]",
            "cmg_json": "[]",
            "potencia_ch4_json": "[]",
            "potencia_ch6_json": "[]",
            "ingreso_json": "[]",
            "p_char_5_json": "[]",
            "error_message": error_message,
        }

    def _build_config_snapshot_fields(self, config_actual: dict) -> dict:
        return {
            "cfg_c1": config_actual["c1"],
            "cfg_c2": config_actual["c2"],
            "cfg_w": config_actual["w"],
            "cfg_v_max": config_actual["v_max"],
            "cfg_n_particles": config_actual["n_particles"],
            "cfg_max_iter": config_actual["max_iter"],
            "cfg_rendimiento_ch4": config_actual["rendimiento_ch4"],
            "cfg_rendimiento_ch6": config_actual["rendimiento_ch6"],
            "cfg_v_inicio_factor": config_actual["v_inicio_factor"],
            "cfg_v_final_factor": config_actual["v_final_factor"],
            "cfg_v_cincel_max": config_actual["v_cincel_max"],
            "cfg_v_cincel_min": config_actual["v_cincel_min"],
            "cfg_v_campanario_max": config_actual["v_campanario_max"],
            "cfg_v_campanario_min": config_actual["v_campanario_min"],
            "cfg_q_rango_min": config_actual["q_rango_min"],
            "cfg_q_rango_max": config_actual["q_rango_max"],
        }

    def _build_user_audit_fields(self, payload) -> dict:
        return {
            "usuario_id": payload.usuario_id,
            "usuario_username": payload.usuario_username,
            "usuario_rol": payload.usuario_rol,
        }

    def _build_success_response(
        self,
        corrida_id: str,
        payload,
        wrapper_result: PSOWrapperOutput,
    ) -> dict:
        return {
            "status": "accepted",
            "message": "Corrida registrada correctamente",
            "data": {
                "id": corrida_id,
                "caso_estudio": payload.caso_estudio,
                "estado": "completada",
                "modo_operacion": payload.modo_operacion,
                "fecha_proceso": payload.fecha_proceso,
                "escenario": payload.escenario,
                "origen_datos": payload.origen_datos,
                "observaciones": payload.observaciones,
                "version_modelo": wrapper_result.version_modelo,
                "modo_ejecucion": wrapper_result.modo_ejecucion,
                "mensaje_modelo": wrapper_result.mensaje_modelo,
                "best_cost": wrapper_result.best_cost,
                "execution_time_sec": wrapper_result.execution_time_sec,
                "q_opt": wrapper_result.q_opt,
                "corrida_base_id": getattr(payload, "corrida_base_id", None),
            },
        }

    def _build_configuracion_usada_dict(self, row: Corrida) -> dict:
        return {
            "c1": row.cfg_c1,
            "c2": row.cfg_c2,
            "w": row.cfg_w,
            "v_max": row.cfg_v_max,
            "n_particles": row.cfg_n_particles,
            "max_iter": row.cfg_max_iter,
            "rendimiento_ch4": row.cfg_rendimiento_ch4,
            "rendimiento_ch6": row.cfg_rendimiento_ch6,
            "v_inicio_factor": row.cfg_v_inicio_factor,
            "v_final_factor": row.cfg_v_final_factor,
            "v_cincel_max": row.cfg_v_cincel_max,
            "v_cincel_min": row.cfg_v_cincel_min,
            "v_campanario_max": row.cfg_v_campanario_max,
            "v_campanario_min": row.cfg_v_campanario_min,
            "q_rango_min": row.cfg_q_rango_min,
            "q_rango_max": row.cfg_q_rango_max,
        }

    def _build_manual_input_payload_json(self, payload: CrearCorridaManualInput) -> str:
        return json.dumps(
            {
                "tipo_input": "manual",
                "modo_operacion": payload.modo_operacion,
                "origen_datos": payload.origen_datos,
                "q_salida_campanario": payload.q_salida_campanario,
                "series": {
                    "cmg": payload.cmg,
                    "p_char_5": payload.p_char_5,
                },
                "metadata": {
                    "caso_estudio": payload.caso_estudio,
                    "fecha_proceso": payload.fecha_proceso,
                    "escenario": payload.escenario,
                    "observaciones": payload.observaciones,
                    "corrida_base_id": payload.corrida_base_id,
                },
            }
        )

    def _ejecutar_engine_input(
        self,
        *,
        engine_input: EngineInputContract,
        escenario: str,
        origen_datos: str,
    ) -> PSOWrapperOutput:
        try:
            resultado = run_pso_engine(
                horas=engine_input.horas,
                q_rango=(
                    engine_input.restricciones.q_rango_min,
                    engine_input.restricciones.q_rango_max,
                ),
                q_cincel=np.array(engine_input.series.q_cincel, dtype=np.float64),
                q_salida_campanario=engine_input.restricciones.q_salida_campanario,
                p_char_5=np.array(engine_input.series.p_char_5, dtype=np.float64),
                v_cincel_inicio=engine_input.restricciones.v_cincel_inicio,
                v_campanario_inicio=engine_input.restricciones.v_campanario_inicio,
                v_cincel_final=engine_input.restricciones.v_cincel_final,
                v_campanario_final=engine_input.restricciones.v_campanario_final,
                v_cincel_max=engine_input.restricciones.v_cincel_max,
                v_cincel_min=engine_input.restricciones.v_cincel_min,
                v_campanario_max=engine_input.restricciones.v_campanario_max,
                v_campanario_min=engine_input.restricciones.v_campanario_min,
                rendimiento_ch4=engine_input.restricciones.rendimiento_ch4,
                rendimiento_ch6=engine_input.restricciones.rendimiento_ch6,
                costo_marginal=np.array(engine_input.series.costo_marginal, dtype=np.float64),
                n_particles=engine_input.configuracion_pso.n_particles,
                max_iter=engine_input.configuracion_pso.max_iter,
                c1=engine_input.configuracion_pso.c1,
                c2=engine_input.configuracion_pso.c2,
                w=engine_input.configuracion_pso.w,
                v_max=engine_input.configuracion_pso.v_max,
            )

            return PSOWrapperOutput(
                estado="completada",
                version_modelo="pso-engine-v1",
                modo_ejecucion="normal",
                mensaje_modelo=(
                    f"Corrida ejecutada con motor PSO real controlado para escenario "
                    f"'{escenario}' y origen '{origen_datos}'."
                ),
                best_cost=resultado["best_cost"],
                execution_time_sec=resultado["execution_time_sec"],
                q_opt=[float(x) for x in resultado["q_opt"]],
                v_cincel=[float(x) for x in resultado["v_cincel"]],
                v_campanario=[float(x) for x in resultado["v_campanario"]],
                cmg=[float(x) for x in resultado["cmg"]],
                potencia_ch4=[float(x) for x in resultado["potencia_ch4"]],
                potencia_ch6=[float(x) for x in resultado["potencia_ch6"]],
                ingreso=[float(x) for x in resultado["ingreso"]],
                q_salida_campanario=float(resultado["q_salida_campanario"]),
                p_char_5=[float(x) for x in resultado["p_char_5"]],
            )
        except PSOValidationError:
            raise
        except Exception as exc:
            raise PSOExecutionError(
                f"Error durante la ejecución del motor PSO: {exc}"
            ) from exc