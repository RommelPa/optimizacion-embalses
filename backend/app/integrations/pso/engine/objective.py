import numpy as np

from app.integrations.pso.engine.repair import reparar_solucion_inteligente
from app.integrations.pso.engine.simulation import (
    calcular_volumenes_con_caudales,
    verificar_violaciones,
)


def funcion_objetivo_unificada(
    positions: np.ndarray,
    horas: int,
    q_rango: tuple[float, float],
    q_cincel: np.ndarray,
    q_salida_campanario: float,
    v_cincel_inicio: float,
    v_campanario_inicio: float,
    v_cincel_final: float,
    v_campanario_final: float,
    v_cincel_max: float,
    v_cincel_min: float,
    v_campanario_max: float,
    v_campanario_min: float,
    rendimiento_ch4: float,
    rendimiento_ch6: float,
    costo_marginal: np.ndarray,
):
    n_particles = positions.shape[0]
    costos_totales = np.zeros(n_particles, dtype=np.float64)

    for i in range(n_particles):
        q_reparado = reparar_solucion_inteligente(
            q_prop=positions[i],
            horas=horas,
            q_rango=q_rango,
            q_cincel=q_cincel,
            q_salida_campanario=q_salida_campanario,
            v_cincel_inicio=v_cincel_inicio,
            v_campanario_inicio=v_campanario_inicio,
            v_cincel_final=v_cincel_final,
            v_cincel_max=v_cincel_max,
            v_cincel_min=v_cincel_min,
            v_campanario_max=v_campanario_max,
            v_campanario_min=v_campanario_min,
        )

        v_cincel, v_campanario, q_ch4, q_ch6 = calcular_volumenes_con_caudales(
            q_salida_cincel=q_reparado,
            horas=horas,
            v_cincel_inicio=v_cincel_inicio,
            v_campanario_inicio=v_campanario_inicio,
            q_cincel=q_cincel,
            q_salida_campanario=q_salida_campanario,
        )

        potencia_ch4 = rendimiento_ch4 * q_ch4
        potencia_ch6 = rendimiento_ch6 * q_ch6

        ingresos = 0.5 * np.sum(
            (potencia_ch4 + potencia_ch6) * costo_marginal,
            dtype=np.float64,
        )
        costos_base = -ingresos

        violaciones = verificar_violaciones(
            v_cincel=v_cincel,
            v_campanario=v_campanario,
            v_cincel_max=v_cincel_max,
            v_cincel_min=v_cincel_min,
            v_campanario_max=v_campanario_max,
            v_campanario_min=v_campanario_min,
        )

        penal_volumenes = 0.0

        if violaciones["Cincel_sobre_max"] > 0:
            penal_volumenes += 1e8 * violaciones["Cincel_sobre_max"]
            penal_volumenes += 1e6 * violaciones["Cincel_max_exceso"]

        if violaciones["Cincel_bajo_min"] > 0:
            penal_volumenes += 1e8 * violaciones["Cincel_bajo_min"]
            penal_volumenes += 1e6 * violaciones["Cincel_min_deficit"]

        if violaciones["Campanario_sobre_max"] > 0:
            penal_volumenes += 1e8 * violaciones["Campanario_sobre_max"]
            penal_volumenes += 1e6 * violaciones["Campanario_max_exceso"]

        if violaciones["Campanario_bajo_min"] > 0:
            penal_volumenes += 1e8 * violaciones["Campanario_bajo_min"]
            penal_volumenes += 1e6 * violaciones["Campanario_min_deficit"]

        if violaciones["Campanario_negativo"] > 0:
            penal_volumenes += 1e10 * violaciones["Campanario_negativo"]

        penal_final = 1e7 * float(
            abs(v_cincel[-1] - v_cincel_final)
            + abs(v_campanario[-1] - v_campanario_final)
        )

        penal_suavidad = 1e4 * np.sum(
            np.square(np.diff(q_reparado)),
            dtype=np.float64,
        )

        costos_totales[i] = np.float64(
            costos_base + penal_volumenes + penal_final + penal_suavidad
        )

    return costos_totales