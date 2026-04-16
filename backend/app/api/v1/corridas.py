from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from app.application.errors import (
    CorridaExecutionAppError,
    CorridaNotFoundError,
    CorridaValidationAppError,
)
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.application.corrida_service import CorridaService
from app.application.dto import CrearCorridaInput
from app.db.session import SessionLocal

router = APIRouter()


class CorridaCreateRequest(BaseModel):
    caso_estudio: str = Field(..., examples=["Base abril 2026 - programa inicial"])
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
    caso_estudio: str
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
    caso_estudio: str
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
    caso_estudio: str
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
    q_salida_campanario: float
    q_opt: list[float]
    v_cincel: list[float]
    v_campanario: list[float]
    cmg: list[float]
    potencia_ch4: list[float]
    potencia_ch6: list[float]
    ingreso: list[float]
    p_char_5: list[float]
    input_payload_json: str
    error_message: Optional[str] = None


@router.post("/corridas", response_model=CorridaCreateResponse)
def crear_corrida(payload: CorridaCreateRequest):
    db = SessionLocal()
    try:
        service = CorridaService(db)

        result = service.crear_corrida(
            CrearCorridaInput(
                caso_estudio=payload.caso_estudio,
                modo_operacion=payload.modo_operacion,
                fecha_proceso=payload.fecha_proceso,
                escenario=payload.escenario,
                origen_datos=payload.origen_datos,
                observaciones=payload.observaciones,
                archivo_entrada=payload.archivo_entrada,
            )
        )

        return CorridaCreateResponse(**result)
    except CorridaValidationAppError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except CorridaExecutionAppError as exc:
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
        service = CorridaService(db)
        result = service.listar_corridas(
            origen_datos=origen_datos,
            estado=estado,
            id_contains=id_contains,
            fecha_proceso=fecha_proceso,
        )
        return CorridaListResponse(**result)
    finally:
        db.close()


@router.get("/corridas/{corrida_id}", response_model=CorridaDetailResponse)
def obtener_corrida(corrida_id: str):
    db = SessionLocal()
    try:
        service = CorridaService(db)
        result = service.obtener_corrida(corrida_id)
        return CorridaDetailResponse(**result)
    except CorridaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        db.close()


@router.get("/corridas/{corrida_id}/export/xlsx")
def exportar_corrida_excel(corrida_id: str):
    db = SessionLocal()
    try:
        service = CorridaService(db)
        content, filename = service.exportar_corrida_excel(corrida_id)

        return Response(
            content=content,
            media_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
            headers={
                "Content-Disposition": f'attachment; filename=\"{filename}\"'
            },
        )
    except CorridaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        db.close()