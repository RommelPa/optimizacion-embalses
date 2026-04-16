from pathlib import Path

import pandas as pd

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
from app.integrations.pso.engine_input_contract import (
    ConfiguracionPSOInput,
    EngineInputContract,
    RestriccionesInput,
    SeriesInput,
)
from app.integrations.pso.errors import PSOValidationError


def build_engine_input_from_excel(
    file_path: str | Path,
    modo_operacion: str = "inicial",
    fecha_proceso: str = "2026-04-08",
    origen_datos: str = "excel",
) -> EngineInputContract:
    file_path = Path(file_path)

    if not file_path.exists():
        raise PSOValidationError(
            f"No se encontró el archivo de entrada: {file_path}"
        )

    try:
        datos_excel = pd.read_excel(file_path, engine="openpyxl")
    except Exception as exc:
        raise PSOValidationError(
            f"No se pudo leer el archivo Excel: {exc}"
        ) from exc

    columnas_requeridas = {"CMG", "P_CHAR 5"}
    columnas_faltantes = columnas_requeridas - set(datos_excel.columns)
    if columnas_faltantes:
        raise PSOValidationError(
            f"Faltan columnas requeridas en Excel: {sorted(columnas_faltantes)}"
        )

    try:
        costo_marginal = datos_excel["CMG"].values[:48].astype(float).tolist()
        p_char_5 = datos_excel["P_CHAR 5"].values[:48].astype(float).tolist()
        q_cincel = (datos_excel["P_CHAR 5"].values[:48].astype(float) / 5.98).tolist()
    except Exception as exc:
        raise PSOValidationError(
            f"No se pudieron convertir las series CMG o P_CHAR 5: {exc}"
        ) from exc

    if len(costo_marginal) < 48 or len(p_char_5) < 48 or len(q_cincel) < 48:
        raise PSOValidationError(
            "El archivo Excel no contiene al menos 48 registros válidos para CMG y P_CHAR 5"
        )

    try:
        df_raw = pd.read_excel(file_path, header=None, engine="openpyxl")
        q_salida_campanario = float(df_raw.iloc[51, 2])
    except Exception as exc:
        raise PSOValidationError(
            f"No se pudo leer q_salida_campanario desde la celda esperada [51,2]: {exc}"
        ) from exc

    series = SeriesInput(
        q_cincel=q_cincel,
        p_char_5=p_char_5,
        costo_marginal=costo_marginal,
    )

    restricciones = RestriccionesInput(
        q_salida_campanario=q_salida_campanario,
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
            f"El contrato de entrada del motor no pudo construirse: {exc}"
        ) from exc