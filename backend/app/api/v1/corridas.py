from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.integrations.pso.contracts import PSOWrapperInput
from app.integrations.pso.wrapper import ejecutar_corrida_pso
from app.integrations.pso.errors import PSOExecutionError, PSOValidationError

import json

from app.db.session import SessionLocal
from app.models.corrida import Corrida

router = APIRouter()


class CorridaCreateRequest(BaseModel):
    modo_operacion: str = Field(..., examples=["inicial"])
    fecha_proceso: str = Field(..., examples=["2026-04-08"])
    escenario: str = Field(..., examples=["base"])
    origen_datos: str = Field(..., examples=["manual"])
    observaciones: Optional[str] = Field(
        default=None,
        examples=["Primera corrida refinada"],
    )
    archivo_entrada: Optional[str] = Field(
        default=None,
        examples=["../data_samples/Datos_Entrada.xlsx"],
    )


class CorridaDataResponse(BaseModel):
    id: str
    estado: str
    modo_operacion: str
    fecha_proceso: str
    escenario: str
    origen_datos: str
    observaciones: Optional[str] = None
    version_modelo: str
    modo_ejecucion: str
    mensaje_modelo: str
    best_cost: float
    execution_time_sec: float
    q_opt: list[float]


class CorridaCreateResponse(BaseModel):
    status: str
    message: str
    data: CorridaDataResponse

class CorridaListItemResponse(BaseModel):
    id: str
    created_at: str
    fecha_proceso: str
    modo_operacion: str
    escenario: str
    origen_datos: str
    estado: str
    version_modelo: str
    modo_ejecucion: str
    best_cost: float
    execution_time_sec: float

class CorridaListResponse(BaseModel):
    items: list[CorridaListItemResponse]
    total: int

class CorridaDetailResponse(BaseModel):
    id: str
    created_at: str
    fecha_proceso: str
    modo_operacion: str
    escenario: str
    origen_datos: str
    observaciones: Optional[str] = None

    estado: str
    version_modelo: str
    modo_ejecucion: str
    mensaje_modelo: str

    best_cost: float
    execution_time_sec: float
    q_opt: list[float]

    input_payload_json: str
    error_message: Optional[str] = None

@router.post("/corridas", response_model=CorridaCreateResponse)
def crear_corrida(payload: CorridaCreateRequest):
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

    input_payload_json = json.dumps(payload.model_dump())

    db = SessionLocal()
    try:
        try:
            wrapper_result = ejecutar_corrida_pso(wrapper_input)

            corrida_db = Corrida(
                id=corrida_id,
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
                q_opt_json=json.dumps(wrapper_result.q_opt),
                input_payload_json=input_payload_json,
                error_message=None,
            )
            db.add(corrida_db)
            db.commit()

            return CorridaCreateResponse(
                status="accepted",
                message="Corrida registrada correctamente",
                data=CorridaDataResponse(
                    id=corrida_id,
                    estado=wrapper_result.estado,
                    modo_operacion=payload.modo_operacion,
                    fecha_proceso=payload.fecha_proceso,
                    escenario=payload.escenario,
                    origen_datos=payload.origen_datos,
                    observaciones=payload.observaciones,
                    version_modelo=wrapper_result.version_modelo,
                    modo_ejecucion=wrapper_result.modo_ejecucion,
                    mensaje_modelo=wrapper_result.mensaje_modelo,
                    best_cost=wrapper_result.best_cost,
                    execution_time_sec=wrapper_result.execution_time_sec,
                    q_opt=wrapper_result.q_opt,
                ),
            )

        except PSOValidationError as exc:
            corrida_db = Corrida(
                id=corrida_id,
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
                q_opt_json="[]",
                input_payload_json=input_payload_json,
                error_message=str(exc),
            )
            db.add(corrida_db)
            db.commit()
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        except PSOExecutionError as exc:
            corrida_db = Corrida(
                id=corrida_id,
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
                q_opt_json="[]",
                input_payload_json=input_payload_json,
                error_message=str(exc),
            )
            db.add(corrida_db)
            db.commit()
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    finally:
        db.close()

@router.get("/corridas", response_model=CorridaListResponse)
def listar_corridas(
    origen_datos: Optional[str] = Query(default=None),
    estado: Optional[str] = Query(default=None),
    id_contains: Optional[str] = Query(default=None),
    fecha_proceso: Optional[str] = Query(default=None),
):
    db = SessionLocal()
    try:
        query = db.query(Corrida)

        if origen_datos:
            query = query.filter(Corrida.origen_datos == origen_datos)

        if estado:
            query = query.filter(Corrida.estado == estado)

        if fecha_proceso:
            query = query.filter(Corrida.fecha_proceso == fecha_proceso)

        if id_contains:
            query = query.filter(Corrida.id.contains(id_contains))

        rows = query.order_by(Corrida.created_at.desc()).all()

        items = [
            CorridaListItemResponse(
                id=row.id,
                created_at=row.created_at.isoformat(),
                fecha_proceso=row.fecha_proceso,
                modo_operacion=row.modo_operacion,
                escenario=row.escenario,
                origen_datos=row.origen_datos,
                estado=row.estado,
                version_modelo=row.version_modelo,
                modo_ejecucion=row.modo_ejecucion,
                best_cost=row.best_cost,
                execution_time_sec=row.execution_time_sec,
            )
            for row in rows
        ]

        return CorridaListResponse(
            items=items,
            total=len(items),
        )
    finally:
        db.close()

@router.get("/corridas/{corrida_id}", response_model=CorridaDetailResponse)
def obtener_corrida(corrida_id: str):
    db = SessionLocal()
    try:
        row = db.query(Corrida).filter(Corrida.id == corrida_id).first()

        if not row:
            raise HTTPException(status_code=404, detail="Corrida no encontrada")

        return CorridaDetailResponse(
            id=row.id,
            created_at=row.created_at.isoformat(),
            fecha_proceso=row.fecha_proceso,
            modo_operacion=row.modo_operacion,
            escenario=row.escenario,
            origen_datos=row.origen_datos,
            observaciones=row.observaciones,
            estado=row.estado,
            version_modelo=row.version_modelo,
            modo_ejecucion=row.modo_ejecucion,
            mensaje_modelo=row.mensaje_modelo,
            best_cost=row.best_cost,
            execution_time_sec=row.execution_time_sec,
            q_opt=json.loads(row.q_opt_json),
            input_payload_json=row.input_payload_json,
            error_message=row.error_message,
        )
    finally:
        db.close()