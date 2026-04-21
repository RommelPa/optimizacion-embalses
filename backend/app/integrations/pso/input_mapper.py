from app.integrations.pso.contracts import PSOWrapperInput
from app.integrations.pso.engine_input_contract import EngineInputContract
from app.integrations.pso.errors import PSOValidationError
from app.integrations.pso.excel_reader import build_engine_input_from_excel


def build_engine_input_from_wrapper(payload: PSOWrapperInput) -> EngineInputContract:
    """
    Construye un contrato validado para el motor PSO a partir del input del wrapper.

    Reglas V1:
    - modo_operacion permitido: 'inicial'
    - origen_datos permitido: 'excel'
    """

    if payload.modo_operacion != "inicial":
        raise PSOValidationError(
            "La V1 solo soporta modo_operacion = 'inicial'."
        )

    if payload.origen_datos != "excel":
        raise PSOValidationError(
            "La V1 solo soporta origen_datos = 'excel'."
        )

    if not payload.archivo_entrada:
        raise PSOValidationError(
            "archivo_entrada es obligatorio cuando origen_datos = 'excel'."
        )

    return build_engine_input_from_excel(
        file_path=payload.archivo_entrada,
        modo_operacion=payload.modo_operacion,
        fecha_proceso=payload.fecha_proceso,
        origen_datos=payload.origen_datos,
    )