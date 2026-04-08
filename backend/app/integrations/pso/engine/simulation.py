import numpy as np


def calcular_volumenes_con_caudales(
    q_salida_cincel: np.ndarray,
    horas: int,
    v_cincel_inicio: float,
    v_campanario_inicio: float,
    q_cincel: np.ndarray,
    q_salida_campanario: float,
):
    q_salida_cincel = np.asarray(q_salida_cincel, dtype=np.float64)

    v_cincel = np.empty(horas + 1, dtype=np.float64)
    v_campanario = np.empty(horas + 1, dtype=np.float64)
    q_ch4 = np.empty(horas, dtype=np.float64)
    q_ch6 = np.empty(horas, dtype=np.float64)

    v_cincel[0] = v_cincel_inicio
    v_campanario[0] = v_campanario_inicio

    for t in range(horas):
        v_cincel[t + 1] = v_cincel[t] + (q_cincel[t] - q_salida_cincel[t]) * 1800.0

        if t == 0:
            q_t = q_salida_cincel[0]
        else:
            q_t = q_salida_cincel[t - 1]

        q_ch4[t] = q_t
        q_ch6[t] = q_t

        v_campanario[t + 1] = (
            v_campanario[t] + (q_t - q_salida_campanario) * 1800.0
        )

    return v_cincel, v_campanario, q_ch4, q_ch6


def verificar_violaciones(
    v_cincel: np.ndarray,
    v_campanario: np.ndarray,
    v_cincel_max: float,
    v_cincel_min: float,
    v_campanario_max: float,
    v_campanario_min: float,
):
    return {
        "Cincel_sobre_max": np.sum(v_cincel[1:] > v_cincel_max),
        "Cincel_bajo_min": np.sum(v_cincel[1:] < v_cincel_min),
        "Campanario_sobre_max": np.sum(v_campanario[1:] > v_campanario_max),
        "Campanario_bajo_min": np.sum(v_campanario[1:] < v_campanario_min),
        "Cincel_max_exceso": np.maximum(v_cincel[1:] - v_cincel_max, 0).sum(),
        "Cincel_min_deficit": np.maximum(v_cincel_min - v_cincel[1:], 0).sum(),
        "Campanario_max_exceso": np.maximum(v_campanario[1:] - v_campanario_max, 0).sum(),
        "Campanario_min_deficit": np.maximum(v_campanario_min - v_campanario[1:], 0).sum(),
        "Campanario_negativo": np.sum(v_campanario[1:] < 0),
    }