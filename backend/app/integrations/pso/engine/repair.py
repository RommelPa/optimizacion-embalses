import numpy as np
from scipy.ndimage import uniform_filter1d

from app.integrations.pso.engine.simulation import (
    calcular_volumenes_con_caudales,
    verificar_violaciones,
)


def reparar_solucion_inteligente(
    q_prop: np.ndarray,
    horas: int,
    q_rango: tuple[float, float],
    q_cincel: np.ndarray,
    q_salida_campanario: float,
    v_cincel_inicio: float,
    v_campanario_inicio: float,
    v_cincel_final: float,
    v_cincel_max: float,
    v_cincel_min: float,
    v_campanario_max: float,
    v_campanario_min: float,
):
    q_prop = np.asarray(q_prop, dtype=np.float64)

    q_suav = uniform_filter1d(q_prop, size=3, mode="mirror")
    q_suav = np.clip(q_suav, q_rango[0], q_rango[1]).astype(np.float64)

    max_iter = 30
    for iteracion in range(max_iter):
        v_c, v_ca, _, _ = calcular_volumenes_con_caudales(
            q_salida_cincel=q_suav,
            horas=horas,
            v_cincel_inicio=v_cincel_inicio,
            v_campanario_inicio=v_campanario_inicio,
            q_cincel=q_cincel,
            q_salida_campanario=q_salida_campanario,
        )

        viol = verificar_violaciones(
            v_cincel=v_c,
            v_campanario=v_ca,
            v_cincel_max=v_cincel_max,
            v_cincel_min=v_cincel_min,
            v_campanario_max=v_campanario_max,
            v_campanario_min=v_campanario_min,
        )

        if (
            viol["Cincel_sobre_max"] == 0
            and viol["Cincel_bajo_min"] == 0
            and viol["Campanario_sobre_max"] == 0
            and viol["Campanario_bajo_min"] == 0
        ):
            break

        ajuste = np.zeros(horas, dtype=np.float64)

        for t in range(horas):
            idx = t + 1
            if idx < len(v_c):
                if v_c[idx] > v_cincel_max * 0.98:
                    exceso = (v_c[idx] - v_cincel_max) / 1800.0
                    ajuste[t] += min(exceso * 0.3, 1.0)
                elif v_c[idx] < v_cincel_min * 1.02:
                    deficit = (v_cincel_min - v_c[idx]) / 1800.0
                    ajuste[t] -= min(deficit * 0.3, 1.0)

        for t in range(1, horas + 1):
            if t < len(v_ca):
                if v_ca[t] > v_campanario_max * 0.98:
                    exceso = (v_ca[t] - v_campanario_max) / 1800.0
                    if t - 1 >= 0:
                        ajuste[t - 1] -= min(exceso * 0.3, 1.0)
                elif v_ca[t] < v_campanario_min * 1.02:
                    deficit = (v_campanario_min - v_ca[t]) / 1800.0
                    if t - 1 >= 0:
                        ajuste[t - 1] += min(deficit * 0.3, 1.0)

        factor = np.float64(0.7 * (1 - iteracion / max_iter) + 0.3)
        q_suav = q_suav + ajuste * factor
        q_suav = np.clip(q_suav, q_rango[0], q_rango[1])

        if iteracion % 5 == 0:
            promedio = np.mean(q_suav)
            if abs(promedio - q_salida_campanario) > 0.2:
                factor_ajuste = q_salida_campanario / promedio
                q_suav = q_suav * np.float64(factor_ajuste)
                q_suav = np.clip(q_suav, q_rango[0], q_rango[1])

    v_c_final, _, _, _ = calcular_volumenes_con_caudales(
        q_salida_cincel=q_suav,
        horas=horas,
        v_cincel_inicio=v_cincel_inicio,
        v_campanario_inicio=v_campanario_inicio,
        q_cincel=q_cincel,
        q_salida_campanario=q_salida_campanario,
    )

    error_cincel = v_c_final[-1] - v_cincel_final
    if abs(error_cincel) > 1000.0:
        ajuste_final = error_cincel / (1800.0 * horas)
        q_suav = q_suav + np.float64(ajuste_final)
        q_suav = np.clip(q_suav, q_rango[0], q_rango[1])

    q_final = uniform_filter1d(q_suav, size=3, mode="mirror")
    q_final = np.clip(q_final, q_rango[0], q_rango[1]).astype(np.float64)

    return q_final