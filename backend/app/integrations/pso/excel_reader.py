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


COLUMNAS_REQUERIDAS: tuple[str, ...] = ("CMG", "P_CHAR 5")
N_PERIODOS_V1 = 48
Q_SALIDA_CAMPANARIO_ROW = 51
Q_SALIDA_CAMPANARIO_COL = 2


def _leer_excel_tabular(file_path: Path) -> pd.DataFrame:
    try:
        return pd.read_excel(file_path, engine="openpyxl")
    except Exception as exc:
        raise PSOValidationError(f"No se pudo leer el archivo Excel: {exc}") from exc


def _validar_columnas_requeridas(df: pd.DataFrame) -> None:
    columnas_requeridas_set: set[str] = set(COLUMNAS_REQUERIDAS)
    columnas_excel_set: set[str] = {str(col) for col in df.columns}
    columnas_faltantes = columnas_requeridas_set - columnas_excel_set

    if columnas_faltantes:
        raise PSOValidationError(
            f"Faltan columnas requeridas en Excel: {sorted(columnas_faltantes)}"
        )


def _extraer_serie_numerica(
    df: pd.DataFrame,
    nombre_columna: str,
    n_periodos: int,
) -> list[float]:
    if nombre_columna not in df.columns:
        raise PSOValidationError(f"La columna requerida '{nombre_columna}' no existe")

    serie = df[nombre_columna].iloc[:n_periodos]

    if len(serie) < n_periodos:
        raise PSOValidationError(
            f"La columna '{nombre_columna}' no contiene {n_periodos} registros"
        )

    if serie.isnull().any():
        posiciones_nulas = [int(i) + 1 for i, v in enumerate(serie.isnull()) if v]
        raise PSOValidationError(
            f"La columna '{nombre_columna}' contiene valores vacíos en los primeros "
            f"{n_periodos} registros. Posiciones: {posiciones_nulas}"
        )

    try:
        return pd.to_numeric(serie, errors="raise").astype(float).tolist()
    except Exception as exc:
        raise PSOValidationError(
            f"La columna '{nombre_columna}' contiene valores no numéricos válidos: {exc}"
        ) from exc


def _leer_q_salida_campanario(file_path: Path) -> float:
    try:
        df_raw = pd.read_excel(file_path, header=None, engine="openpyxl")
    except Exception as exc:
        raise PSOValidationError(
            f"No se pudo leer el archivo Excel para obtener q_salida_campanario: {exc}"
        ) from exc

    try:
        valor = df_raw.iloc[Q_SALIDA_CAMPANARIO_ROW, Q_SALIDA_CAMPANARIO_COL]
    except Exception as exc:
        raise PSOValidationError(
            "No se pudo acceder a la celda esperada para q_salida_campanario "
            f"[{Q_SALIDA_CAMPANARIO_ROW},{Q_SALIDA_CAMPANARIO_COL}]"
        ) from exc

    if pd.isna(valor):
        raise PSOValidationError(
            "La celda esperada de q_salida_campanario está vacía"
        )

    try:
        valor_float = float(str(valor).strip())
    except Exception as exc:
        raise PSOValidationError(
            f"q_salida_campanario no es numérico: {valor}"
        ) from exc

    if valor_float <= 0:
        raise PSOValidationError(
            "q_salida_campanario debe ser mayor a 0"
        )

    return valor_float


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

    df = _leer_excel_tabular(file_path)
    _validar_columnas_requeridas(df)

    costo_marginal = _extraer_serie_numerica(df, "CMG", N_PERIODOS_V1)
    p_char_5 = _extraer_serie_numerica(df, "P_CHAR 5", N_PERIODOS_V1)
    q_cincel = [valor / 5.98 for valor in p_char_5]

    q_salida_campanario = _leer_q_salida_campanario(file_path)

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