from app.integrations.pso.config import (
    DEFAULT_MAX_ITER,
    DEFAULT_N_PARTICLES,
    DEFAULT_V_FINAL_FACTOR,
    DEFAULT_V_INICIO_FACTOR,
    Q_RANGO_MAX,
    Q_RANGO_MIN,
    RENDIMIENTO_CH4,
    RENDIMIENTO_CH6,
    V_CAMPANARIO_MAX,
    V_CAMPANARIO_MIN,
    V_CINCEL_MAX,
    V_CINCEL_MIN,
)
from app.integrations.pso.contracts import PSOWrapperInput
from app.integrations.pso.engine_input_contract import (
    ConfiguracionPSOInput,
    EngineInputContract,
    RestriccionesInput,
    SeriesInput,
)
from app.integrations.pso.excel_reader import build_engine_input_from_excel


def build_engine_input_from_wrapper(payload: PSOWrapperInput) -> EngineInputContract:
    """
    Construye un contrato validado para el motor PSO a partir del input del wrapper.

    Reglas actuales:
    - origen_datos = "excel" -> usa lector real de Excel
    - otros orígenes -> usa escenario controlado
    """

    if payload.origen_datos == "excel":
        if not payload.archivo_entrada:
            raise ValueError(
                "archivo_entrada es obligatorio cuando origen_datos = 'excel'"
            )

        return build_engine_input_from_excel(
            file_path=payload.archivo_entrada,
            modo_operacion=payload.modo_operacion,
            fecha_proceso=payload.fecha_proceso,
            origen_datos=payload.origen_datos,
        )

    horas = 4

    q_cincel = [10.0] * horas
    p_char_5 = [round(q * 5.98, 4) for q in q_cincel]

    series = SeriesInput(
        q_cincel=q_cincel,
        p_char_5=p_char_5,
        costo_marginal=[100.0] * horas,
    )

    restricciones = RestriccionesInput(
        q_salida_campanario=10.0,
        v_cincel_inicio=DEFAULT_V_INICIO_FACTOR * V_CINCEL_MAX,
        v_campanario_inicio=DEFAULT_V_INICIO_FACTOR * V_CAMPANARIO_MAX,
        v_cincel_final=DEFAULT_V_FINAL_FACTOR * V_CINCEL_MAX,
        v_campanario_final=DEFAULT_V_FINAL_FACTOR * V_CAMPANARIO_MAX,
        v_cincel_max=V_CINCEL_MAX,
        v_cincel_min=V_CINCEL_MIN,
        v_campanario_max=V_CAMPANARIO_MAX,
        v_campanario_min=V_CAMPANARIO_MIN,
        q_rango_min=Q_RANGO_MIN,
        q_rango_max=Q_RANGO_MAX,
        rendimiento_ch4=RENDIMIENTO_CH4,
        rendimiento_ch6=RENDIMIENTO_CH6,
    )

    configuracion_pso = ConfiguracionPSOInput(
        n_particles=DEFAULT_N_PARTICLES,
        max_iter=DEFAULT_MAX_ITER,
    )

    return EngineInputContract(
        modo_operacion=payload.modo_operacion,
        fecha_proceso=payload.fecha_proceso,
        origen_datos=payload.origen_datos,
        series=series,
        restricciones=restricciones,
        configuracion_pso=configuracion_pso,
    )