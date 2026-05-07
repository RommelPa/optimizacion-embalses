from __future__ import annotations

from app.integrations.pso.engine_input_contract import (
    ConfiguracionPSOInput,
    EngineInputContract,
    RestriccionesInput,
    SeriesInput,
)
from app.integrations.pso.errors import PSOValidationError

N_PERIODOS_V1 = 48
P_CHAR5_A_Q_FACTOR = 5.98

def _normalizar_serie_numerica(
    values: list[float],
    nombre: str,
    *,
    allow_negative: bool = True,
) -> list[float]:
    if not values:
        raise PSOValidationError(f"La serie '{nombre}' no puede estar vacía.")

    if len(values) != N_PERIODOS_V1:
        raise PSOValidationError(
            f"La serie '{nombre}' debe tener exactamente {N_PERIODOS_V1} valores."
        )

    normalizados: list[float] = []
    for idx, value in enumerate(values, start=1):
        try:
            value_float = float(value)
        except (TypeError, ValueError) as exc:
            raise PSOValidationError(
                f"La serie '{nombre}' contiene un valor no numérico en la posición {idx}."
            ) from exc

        if not allow_negative and value_float < 0:
            raise PSOValidationError(
                f"La serie '{nombre}' no puede contener valores negativos."
            )

        normalizados.append(value_float)

    return normalizados


def build_engine_input_from_manual(
    *,
    q_salida_campanario: float,
    cmg: list[float],
    p_char_5: list[float],
    configuracion: dict,
    modo_operacion: str = "inicial",
    fecha_proceso: str,
    origen_datos: str = "manual",
) -> EngineInputContract:
    if modo_operacion != "inicial":
        raise PSOValidationError(
            "La V1.4 solo soporta modo_operacion = 'inicial' para carga manual."
        )

    if origen_datos != "manual":
        raise PSOValidationError(
            "La construcción manual solo soporta origen_datos = 'manual'."
        )

    try:
        q_salida_campanario = float(q_salida_campanario)
    except (TypeError, ValueError) as exc:
        raise PSOValidationError("q_salida_campanario debe ser numérico.") from exc

    if q_salida_campanario <= 0:
        raise PSOValidationError("q_salida_campanario debe ser mayor a 0.")

    costo_marginal = _normalizar_serie_numerica(cmg, "CMG", allow_negative=True)
    p_char_5_normalizada = _normalizar_serie_numerica(
        p_char_5,
        "P_CHAR 5",
        allow_negative=False,
    )
    q_cincel = [valor / P_CHAR5_A_Q_FACTOR for valor in p_char_5_normalizada]

    v_cincel_max = float(configuracion["v_cincel_max"])
    v_cincel_min = float(configuracion["v_cincel_min"])
    v_campanario_max = float(configuracion["v_campanario_max"])
    v_campanario_min = float(configuracion["v_campanario_min"])
    q_rango_min = float(configuracion["q_rango_min"])
    q_rango_max = float(configuracion["q_rango_max"])
    rendimiento_ch4 = float(configuracion["rendimiento_ch4"])
    rendimiento_ch6 = float(configuracion["rendimiento_ch6"])
    v_inicio_factor = float(configuracion["v_inicio_factor"])
    v_final_factor = float(configuracion["v_final_factor"])
    n_particles = int(configuracion["n_particles"])
    max_iter = int(configuracion["max_iter"])

    if q_rango_min >= q_rango_max:
        raise PSOValidationError("La configuración actual tiene un rango de caudal inválido.")

    if v_cincel_min >= v_cincel_max:
        raise PSOValidationError("La configuración actual tiene límites inválidos para Cincel.")

    if v_campanario_min >= v_campanario_max:
        raise PSOValidationError(
            "La configuración actual tiene límites inválidos para Campanario."
        )

    series = SeriesInput(
        q_cincel=q_cincel,
        p_char_5=p_char_5_normalizada,
        costo_marginal=costo_marginal,
    )

    restricciones = RestriccionesInput(
        q_salida_campanario=q_salida_campanario,
        v_cincel_inicio=v_inicio_factor * v_cincel_max,
        v_campanario_inicio=v_inicio_factor * v_campanario_max,
        v_cincel_final=v_final_factor * v_cincel_max,
        v_campanario_final=v_final_factor * v_campanario_max,
        v_cincel_max=v_cincel_max,
        v_cincel_min=v_cincel_min,
        v_campanario_max=v_campanario_max,
        v_campanario_min=v_campanario_min,
        q_rango_min=q_rango_min,
        q_rango_max=q_rango_max,
        rendimiento_ch4=rendimiento_ch4,
        rendimiento_ch6=rendimiento_ch6,
    )

    configuracion_pso = ConfiguracionPSOInput(
        n_particles=n_particles,
        max_iter=max_iter,
        c1=float(configuracion["c1"]),
        c2=float(configuracion["c2"]),
        w=float(configuracion["w"]),
        v_max=float(configuracion["v_max"]),
    )

    try:
        return EngineInputContract(
            modo_operacion=modo_operacion,  # type: ignore[arg-type]
            fecha_proceso=fecha_proceso,
            origen_datos=origen_datos,  # type: ignore[arg-type]
            series=series,
            restricciones=restricciones,
            configuracion_pso=configuracion_pso,
        )
    except Exception as exc:
        raise PSOValidationError(
            f"El contrato manual no pudo construirse: {exc}"
        ) from exc