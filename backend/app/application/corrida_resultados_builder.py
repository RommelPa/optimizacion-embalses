from __future__ import annotations

import json
from typing import Any

import numpy as np

from app.models.corrida import Corrida

P_CHAR5_A_Q_FACTOR = 5.98


def generar_etiquetas_hora(n_periodos: int) -> list[str]:
    etiquetas: list[str] = []
    for i in range(n_periodos):
        minutos = (i + 1) * 30
        h = (minutos // 60) % 24
        m = minutos % 60
        etiquetas.append("24:00" if h == 0 and m == 0 else f"{h:02d}:{m:02d}")
    return etiquetas


def generar_etiquetas_desde_periodo(periodo_inicio: int, n_periodos: int) -> list[str]:
    etiquetas: list[str] = []
    for i in range(n_periodos):
        p = periodo_inicio + i + 1
        minutos = p * 30
        h = (minutos // 60) % 24
        m = minutos % 60
        etiquetas.append("24:00" if h == 0 and m == 0 else f"{h:02d}:{m:02d}")
    return etiquetas


def calcular_correlacion(cmg: list[float], potencia_total: list[float]) -> float:
    if len(cmg) <= 1 or len(potencia_total) <= 1:
        return 0.0

    try:
        correlacion = float(np.corrcoef(cmg, potencia_total)[0, 1])
        return 0.0 if np.isnan(correlacion) else correlacion
    except Exception:
        return 0.0


def _build_titulo_modo(modo_operacion: str) -> str:
    return "REPROGRAMA" if modo_operacion == "reprograma" else "PROGRAMA INICIAL"


def _safe_json_load(value: str | None, default: list[Any] | None = None) -> list[Any]:
    if default is None:
        default = []

    if not value:
        return default

    try:
        loaded = json.loads(value)
        return loaded if isinstance(loaded, list) else default
    except Exception:
        return default


def build_resultados_dataset(corrida: Corrida) -> dict[str, Any]:
    q_opt = _safe_json_load(corrida.q_opt_json)
    v_cincel = _safe_json_load(corrida.v_cincel_json)
    v_campanario = _safe_json_load(corrida.v_campanario_json)
    cmg = _safe_json_load(corrida.cmg_json)
    potencia_ch4 = _safe_json_load(corrida.potencia_ch4_json)
    potencia_ch6 = _safe_json_load(corrida.potencia_ch6_json)
    ingreso = _safe_json_load(corrida.ingreso_json)
    p_char_5 = _safe_json_load(corrida.p_char_5_json)

    horas = len(q_opt)
    periodos = list(range(1, horas + 1))
    horas_etiquetas = generar_etiquetas_hora(horas)
    etiquetas_todas = generar_etiquetas_desde_periodo(0, horas)
    tick_step = 4 if horas >= 8 else 1

    q_salida_campanario = float(corrida.q_salida_campanario)
    titulo_modo = _build_titulo_modo(corrida.modo_operacion)

    q_entrada_cincel = [
        float(value) / P_CHAR5_A_Q_FACTOR
        for value in p_char_5[:horas]
    ]

    v_cincel_operativo = [
        float(value) for value in v_cincel[1 : horas + 1]
    ] if len(v_cincel) > 1 else []

    v_campanario_operativo = [
        float(value) for value in v_campanario[1 : horas + 1]
    ] if len(v_campanario) > 1 else []

    potencia_total = [
        (float(potencia_ch4[i]) if i < len(potencia_ch4) else 0.0)
        + (float(potencia_ch6[i]) if i < len(potencia_ch6) else 0.0)
        for i in range(horas)
    ]
    correlacion = calcular_correlacion(
        [float(x) for x in cmg[:horas]],
        potencia_total,
    )

    ch123 = [6.6 if q_salida_campanario >= 10.0 else None for _ in range(horas)]

    tabla_rows: list[dict[str, Any]] = []
    for i in range(horas):
        tabla_rows.append(
            {
                "hora": horas_etiquetas[i],
                "p_char_5": float(p_char_5[i]) if i < len(p_char_5) else None,
                "v_cincel": float(v_cincel[i + 1]) if i + 1 < len(v_cincel) else None,
                "q_opt": float(q_opt[i]) if i < len(q_opt) else None,
                "v_campanario": float(v_campanario[i + 1]) if i + 1 < len(v_campanario) else None,
                "q_salida_campanario": q_salida_campanario,
                "potencia_ch4": float(potencia_ch4[i]) if i < len(potencia_ch4) else None,
                "potencia_ch6": float(potencia_ch6[i]) if i < len(potencia_ch6) else None,
                "ch123": ch123[i] if i < len(ch123) else None,
                "cmg": float(cmg[i]) if i < len(cmg) else None,
                "ingreso": float(ingreso[i]) if i < len(ingreso) else None,
            }
        )

    ingresos_totales = float(sum(float(x) for x in ingreso)) if ingreso else 0.0

    dataset = {
        "meta": {
            "horas": horas,
            "periodos": periodos,
            "horas_etiquetas": horas_etiquetas,
            "etiquetas_todas": etiquetas_todas,
            "tick_step": tick_step,
            "titulo_modo": titulo_modo,
            "q_salida_campanario": q_salida_campanario,
            "correlacion": correlacion,
            "ingresos_totales": ingresos_totales,
        },
        "tabla": {
            "rows": tabla_rows,
        },
        "caudal": {
            "q_opt": [float(x) for x in q_opt[:horas]],
            "q_entrada_cincel": q_entrada_cincel,
            "q_referencia": q_salida_campanario,
            "q_rango_min": float(corrida.cfg_q_rango_min),
            "q_rango_max": float(corrida.cfg_q_rango_max),
        },
        "volumenes": {
            "v_cincel": v_cincel_operativo,
            "v_campanario": v_campanario_operativo,
            "v_cincel_min": float(corrida.cfg_v_cincel_min),
            "v_cincel_max": float(corrida.cfg_v_cincel_max),
            "v_campanario_min": float(corrida.cfg_v_campanario_min),
            "v_campanario_max": float(corrida.cfg_v_campanario_max),
        },
        "despacho": {
            "cmg": [float(x) for x in cmg[:horas]],
            "potencia_ch4": [float(x) for x in potencia_ch4[:horas]],
            "potencia_ch6": [float(x) for x in potencia_ch6[:horas]],
            "correlacion": correlacion,
        },
        "validacion": {
            "v_cincel_inicial": float(v_cincel[0]) if v_cincel else 0.0,
            "v_cincel_final": float(v_cincel[-1]) if v_cincel else 0.0,
            "v_campanario_inicial": float(v_campanario[0]) if v_campanario else 0.0,
            "v_campanario_final": float(v_campanario[-1]) if v_campanario else 0.0,
        },
    }
    return dataset