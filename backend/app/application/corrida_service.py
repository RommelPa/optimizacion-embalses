from __future__ import annotations

import json
from uuid import uuid4

from app.application.errors import (
    CorridaExecutionAppError,
    CorridaNotFoundError,
    CorridaValidationAppError,
)
from sqlalchemy.orm import Session

from app.application.dto import CrearCorridaInput
from app.integrations.pso.contracts import PSOWrapperInput
from app.integrations.pso.errors import PSOExecutionError, PSOValidationError
from app.integrations.pso.wrapper import ejecutar_corrida_pso
from app.models.corrida import Corrida
from app.repositories.corrida_repository import CorridaRepository
from app.application.utils import serialize_datetime_utc
from app.application.excel_exporter import build_excel_corrida_legacy

class CorridaService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = CorridaRepository(db)

    def crear_corrida(self, payload: CrearCorridaInput) -> dict:
        corrida_id = str(uuid4())

        wrapper_input = PSOWrapperInput(
            corrida_id=corrida_id,
            modo_operacion=payload.modo_operacion,
            fecha_proceso=payload.fecha_proceso,
            escenario=payload.escenario,
            origen_datos=payload.origen_datos,
            observaciones=payload.observaciones,
            archivo_entrada=payload.archivo_entrada,
        )

        input_payload_json = json.dumps(payload.__dict__)

        try:
            wrapper_result = ejecutar_corrida_pso(wrapper_input)

            corrida_db = Corrida(
                id=corrida_id,
                caso_estudio=payload.caso_estudio,
                fecha_proceso=payload.fecha_proceso,
                modo_operacion=payload.modo_operacion,
                escenario=payload.escenario,
                origen_datos=payload.origen_datos,
                observaciones=payload.observaciones,
                estado=wrapper_result.estado,
                version_modelo=wrapper_result.version_modelo,
                modo_ejecucion=wrapper_result.modo_ejecucion,
                mensaje_modelo=wrapper_result.mensaje_modelo,
                best_cost=wrapper_result.best_cost,
                execution_time_sec=wrapper_result.execution_time_sec,
                q_salida_campanario=wrapper_result.q_salida_campanario,
                q_opt_json=json.dumps(wrapper_result.q_opt),
                v_cincel_json=json.dumps(wrapper_result.v_cincel),
                v_campanario_json=json.dumps(wrapper_result.v_campanario),
                cmg_json=json.dumps(wrapper_result.cmg),
                potencia_ch4_json=json.dumps(wrapper_result.potencia_ch4),
                potencia_ch6_json=json.dumps(wrapper_result.potencia_ch6),
                ingreso_json=json.dumps(wrapper_result.ingreso),
                p_char_5_json=json.dumps(wrapper_result.p_char_5),
                input_payload_json=input_payload_json,
                error_message=None,
            )
            self.repo.add(corrida_db)

            return {
                "status": "accepted",
                "message": "Corrida registrada correctamente",
                "data": {
                    "id": corrida_id,
                    "caso_estudio": payload.caso_estudio,
                    "estado": wrapper_result.estado,
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
                },
            }

        except PSOValidationError as exc:
            corrida_db = Corrida(
                id=corrida_id,
                caso_estudio=payload.caso_estudio,
                fecha_proceso=payload.fecha_proceso,
                modo_operacion=payload.modo_operacion,
                escenario=payload.escenario,
                origen_datos=payload.origen_datos,
                observaciones=payload.observaciones,
                estado="fallida",
                version_modelo="pso-engine-v1",
                modo_ejecucion="error_validacion",
                mensaje_modelo="La corrida falló por error de validación",
                best_cost=0.0,
                execution_time_sec=0.0,
                q_salida_campanario=0.0,
                q_opt_json="[]",
                v_cincel_json="[]",
                v_campanario_json="[]",
                cmg_json="[]",
                potencia_ch4_json="[]",
                potencia_ch6_json="[]",
                ingreso_json="[]",
                p_char_5_json="[]",
                input_payload_json=input_payload_json,
                error_message=str(exc),
            )
            self.repo.add(corrida_db)
            raise CorridaValidationAppError(str(exc)) from exc

        except PSOExecutionError as exc:
            corrida_db = Corrida(
                id=corrida_id,
                caso_estudio=payload.caso_estudio,
                fecha_proceso=payload.fecha_proceso,
                modo_operacion=payload.modo_operacion,
                escenario=payload.escenario,
                origen_datos=payload.origen_datos,
                observaciones=payload.observaciones,
                estado="fallida",
                version_modelo="pso-engine-v1",
                modo_ejecucion="error_ejecucion",
                mensaje_modelo="La corrida falló durante la ejecución del motor",
                best_cost=0.0,
                execution_time_sec=0.0,
                q_salida_campanario=0.0,
                q_opt_json="[]",
                v_cincel_json="[]",
                v_campanario_json="[]",
                cmg_json="[]",
                potencia_ch4_json="[]",
                potencia_ch6_json="[]",
                ingreso_json="[]",
                p_char_5_json="[]",
                input_payload_json=input_payload_json,
                error_message=str(exc),
            )
            self.repo.add(corrida_db)
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
        }
    
    def exportar_corrida_excel(self, corrida_id: str) -> tuple[bytes, str]:
        row = self.repo.get_by_id(corrida_id)

        if not row:
            raise CorridaNotFoundError("Corrida no encontrada")

        return build_excel_corrida_legacy(row)
    