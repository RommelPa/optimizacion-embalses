from __future__ import annotations

import json
import os
import tempfile
from io import BytesIO
from typing import cast

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from app.integrations.pso.config import (
    Q_RANGO_MAX,
    Q_RANGO_MIN,
    V_CAMPANARIO_MAX,
    V_CAMPANARIO_MIN,
    V_CINCEL_MAX,
    V_CINCEL_MIN,
)
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


def insertar_imagen_excel(
    ws: Worksheet,
    image_path: str,
    anchor: str,
    scale: float = 0.55,
) -> None:
    img = Image(image_path)
    img.width = int(img.width * scale)
    img.height = int(img.height * scale)
    img.anchor = anchor
    ws.add_image(img)


def calcular_correlacion(cmg: list[float], potencia_total: list[float]) -> float:
    if len(cmg) <= 1 or len(potencia_total) <= 1:
        return 0.0

    try:
        correlacion = float(np.corrcoef(cmg, potencia_total)[0, 1])
        return 0.0 if np.isnan(correlacion) else correlacion
    except Exception:
        return 0.0


def build_excel_corrida_legacy(corrida: Corrida) -> tuple[bytes, str]:
    wb = Workbook()
    ws = cast(Worksheet, wb.active)
    ws.title = "Resultados"

    q_opt = json.loads(corrida.q_opt_json)
    v_cincel = json.loads(corrida.v_cincel_json)
    v_campanario = json.loads(corrida.v_campanario_json)
    cmg = json.loads(corrida.cmg_json)
    potencia_ch4 = json.loads(corrida.potencia_ch4_json)
    potencia_ch6 = json.loads(corrida.potencia_ch6_json)
    ingreso = json.loads(corrida.ingreso_json)
    p_char_5 = json.loads(corrida.p_char_5_json)

    horas = len(q_opt)
    horas_etiquetas = generar_etiquetas_hora(horas)
    etiquetas_todas = generar_etiquetas_desde_periodo(0, horas)
    periodos = np.arange(1, horas + 1)
    tick_step = 4 if horas >= 8 else 1

    q_salida_campanario = corrida.q_salida_campanario
    titulo_modo = (
        "REPROGRAMA"
        if corrida.modo_operacion == "reprograma"
        else "PROGRAMA INICIAL"
    )

    ch123 = [6.6 if q_salida_campanario >= 10.0 else None for _ in range(horas)]
    ingresos_totales = float(sum(ingreso)) if ingreso else 0.0

    potencia_total = [
        (potencia_ch4[i] if i < len(potencia_ch4) else 0.0)
        + (potencia_ch6[i] if i < len(potencia_ch6) else 0.0)
        for i in range(horas)
    ]
    correlacion = calcular_correlacion(cmg, potencia_total)

    es_valida = False
    if len(v_cincel) > 1 and len(v_campanario) > 1:
        viol_cincel_sobre = sum(1 for x in v_cincel[1:] if x > V_CINCEL_MAX)
        viol_cincel_bajo = sum(1 for x in v_cincel[1:] if x < V_CINCEL_MIN)
        viol_camp_sobre = sum(1 for x in v_campanario[1:] if x > V_CAMPANARIO_MAX)
        viol_camp_bajo = sum(1 for x in v_campanario[1:] if x < V_CAMPANARIO_MIN)
        viol_camp_neg = sum(1 for x in v_campanario[1:] if x < 0)

        es_valida = (
            viol_cincel_sobre == 0
            and viol_cincel_bajo == 0
            and viol_camp_sobre == 0
            and viol_camp_bajo == 0
            and viol_camp_neg == 0
            and abs(v_cincel[-1] - (0.85 * V_CINCEL_MAX)) < 5000
            and abs(v_campanario[-1] - (0.85 * V_CAMPANARIO_MAX)) < 5000
        )

    headers = [
        "HORA",
        "P_Char 5 (MW)",
        "Volumen D. Cincel (m3)",
        "Caudal Salida D. Cincel (m3/s)",
        "Volumen D. Campanario (m3)",
        "Caudal salida D. Campanario (m3/s)",
        "CH 4 (MW)",
        "CH 6 (MW)",
        "CH 123 (MW)",
        "CMG (S/./MWh)",
        "Ingresos",
    ]
    ws.append(headers)

    for i in range(horas):
        ws.append(
            [
                horas_etiquetas[i],
                p_char_5[i] if i < len(p_char_5) else None,
                int(v_cincel[i + 1]) if i + 1 < len(v_cincel) else None,
                round(q_opt[i], 1) if i < len(q_opt) else None,
                int(v_campanario[i + 1]) if i + 1 < len(v_campanario) else None,
                round(q_salida_campanario, 1),
                round(potencia_ch4[i], 1) if i < len(potencia_ch4) else None,
                round(potencia_ch6[i], 1) if i < len(potencia_ch6) else None,
                ch123[i] if i < len(ch123) else None,
                round(cmg[i], 1) if i < len(cmg) else None,
                round(ingreso[i], 2) if i < len(ingreso) else None,
            ]
        )

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="1F497D")
    center_align = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )

    for col in range(1, 12):
        cell = ws.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border

    anchos = [8, 14, 22, 28, 26, 32, 10, 10, 12, 16, 12]
    for i, ancho in enumerate(anchos, start=1):
        ws.column_dimensions[get_column_letter(i)].width = ancho

    for row_idx in range(2, horas + 2):
        for col_idx in range(1, 12):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.alignment = center_align
            cell.border = thin_border

    fila_resumen = horas + 3
    resumen_datos = [
        ("Caso de estudio", corrida.caso_estudio),
        ("Modo", titulo_modo),
        ("Ingresos totales período reopt ($)", round(ingresos_totales, 2)),
        ("Tiempo optimización (min)", round(corrida.execution_time_sec / 60.0, 3)),
        ("Tiempo total (min)", round(corrida.execution_time_sec / 60.0, 3)),
        ("Correlación CMG-Potencia total", round(correlacion, 4)),
        ("Q promedio optimizado (m³/s)", round(sum(q_opt) / len(q_opt), 3) if q_opt else 0),
        ("Vol. D. Cincel inicial (mil m³)", round((v_cincel[0] if v_cincel else 0) / 1000, 1)),
        ("Vol. D. Cincel final (mil m³)", round((v_cincel[-1] if v_cincel else 0) / 1000, 1)),
        ("Vol. D. Campanario inicial (mil m³)", round((v_campanario[0] if v_campanario else 0) / 1000, 1)),
        ("Vol. D. Campanario final (mil m³)", round((v_campanario[-1] if v_campanario else 0) / 1000, 1)),
        ("Solución válida", "SÍ" if es_valida else "NO - REVISAR"),
    ]

    for idx, (etiqueta, valor) in enumerate(resumen_datos):
        ws.cell(row=fila_resumen + idx, column=1, value=etiqueta)
        ws.cell(row=fila_resumen + idx, column=2, value=valor)

    q_opt_arr = np.array(q_opt, dtype=np.float64)
    q_cincel_arr = np.array(p_char_5, dtype=np.float64) / P_CHAR5_A_Q_FACTOR
    v_cincel_arr = np.array(v_cincel[1:], dtype=np.float64)
    v_camp_arr = np.array(v_campanario[1:], dtype=np.float64)
    cmg_arr = np.array(cmg, dtype=np.float64)
    pot_ch4_arr = np.array(potencia_ch4, dtype=np.float64)
    pot_ch6_arr = np.array(potencia_ch6, dtype=np.float64)

    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_caudal = os.path.join(tmpdir, "grafico_caudal.png")
        ruta_cmg = os.path.join(tmpdir, "grafico_cmg_potencia.png")
        ruta_vol = os.path.join(tmpdir, "grafico_volumenes.png")

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(periodos, q_opt_arr, color="tab:blue", linewidth=2.2, label="Q optimizado")
        ax1.plot(
            periodos,
            q_cincel_arr,
            color="darkgreen",
            linestyle="--",
            linewidth=1,
            alpha=0.5,
            label="Q entrada D. Cincel",
        )
        ax1.axhline(
            y=float(np.mean(q_opt_arr)),
            color="r",
            linestyle="--",
            alpha=0.5,
            label=f"Promedio: {np.mean(q_opt_arr):.1f} m³/s",
        )
        ax1.fill_between(
            periodos,
            Q_RANGO_MIN,
            Q_RANGO_MAX,
            color="gray",
            alpha=0.15,
            label="Límites operativos",
        )
        ax1.set_title(
            f"Caudal Salida D. Cincel — {titulo_modo} (Q_Camp={q_salida_campanario:.1f} m³/s)"
        )
        ax1.set_xlabel("Periodo (30 min)")
        ax1.set_ylabel("Caudal (m³/s)")
        ax1.legend(loc="upper left", fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(periodos[::tick_step])
        ax1.set_xticklabels(etiquetas_todas[::tick_step], rotation=45, fontsize=7)
        ax1.set_xlim(0.5, horas + 0.5)
        fig1.tight_layout()
        fig1.savefig(ruta_caudal, dpi=150, bbox_inches="tight")
        plt.close(fig1)

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2_b = ax2.twinx()
        ax2.plot(periodos, cmg_arr, color="tab:red", linewidth=2, label="CMG", alpha=0.9)
        ax2.fill_between(periodos, 0, cmg_arr, color="red", alpha=0.08)
        ax2_b.plot(periodos, pot_ch4_arr, color="tab:blue", linewidth=2, label="Charcani 4", alpha=0.9)
        ax2_b.plot(periodos, pot_ch6_arr, color="tab:green", linewidth=2, linestyle="--", label="Charcani 6", alpha=0.9)
        ax2.set_title(f"Despacho Económico — {titulo_modo} (Corr: {correlacion:.3f})")
        ax2.set_xlabel("Periodo (30 min)")
        ax2.set_ylabel("CMG (S/./MWh)", color="r")
        ax2_b.set_ylabel("Potencia (MW)", color="b")
        ax2.tick_params(axis="y", labelcolor="r")
        ax2_b.tick_params(axis="y", labelcolor="b")
        ax2.legend(loc="upper left", fontsize=8)
        ax2_b.legend(loc="upper right", fontsize=8)
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(periodos[::tick_step])
        ax2.set_xticklabels(etiquetas_todas[::tick_step], rotation=45, fontsize=7)
        ax2.set_xlim(0.5, horas + 0.5)
        fig2.tight_layout()
        fig2.savefig(ruta_cmg, dpi=150, bbox_inches="tight")
        plt.close(fig2)

        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(periodos, v_cincel_arr, color="tab:blue", linewidth=2.2, label="Vol. D. Cincel")
        ax3.plot(periodos, v_camp_arr, color="tab:green", linewidth=2.2, label="Vol. D. Campanario")
        ax3.fill_between(periodos, V_CINCEL_MIN, V_CINCEL_MAX, color="blue", alpha=0.07)
        ax3.fill_between(periodos, V_CAMPANARIO_MIN, V_CAMPANARIO_MAX, color="green", alpha=0.07)
        ax3.axhline(y=V_CINCEL_MAX, color="navy", linestyle=":", linewidth=1, alpha=0.5)
        ax3.axhline(y=V_CINCEL_MIN, color="navy", linestyle=":", linewidth=1, alpha=0.5)
        ax3.axhline(y=V_CAMPANARIO_MAX, color="darkgreen", linestyle=":", linewidth=1, alpha=0.5)
        ax3.axhline(y=V_CAMPANARIO_MIN, color="darkgreen", linestyle=":", linewidth=1, alpha=0.5)
        ax3.set_title(f"Evolución de Volúmenes — {titulo_modo}")
        ax3.set_xlabel("Periodo (30 minutos)")
        ax3.set_ylabel("Volumen (m³)")
        ax3.legend(loc="upper left", fontsize=8)
        ax3.set_xticks(periodos[::tick_step])
        ax3.set_xticklabels(etiquetas_todas[::tick_step], rotation=45, fontsize=7)
        ax3.set_xlim(0.5, horas + 0.5)
        fig3.tight_layout()
        fig3.savefig(ruta_vol, dpi=150, bbox_inches="tight")
        plt.close(fig3)

        insertar_imagen_excel(ws, ruta_caudal, "M2")
        insertar_imagen_excel(ws, ruta_cmg, "M25")
        insertar_imagen_excel(ws, ruta_vol, "M48")

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        filename = f"Resultados_PSO_CH46_Q{int(q_salida_campanario)}.xlsx"
        return output.getvalue(), filename