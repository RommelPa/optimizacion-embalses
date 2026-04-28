from __future__ import annotations

from typing import Any


def _build_tick_positions_and_labels(
    periodos: list[int],
    etiquetas: list[str],
    tick_step: int,
) -> tuple[list[int], list[str]]:
    if not periodos or not etiquetas:
        return [], []

    tick_positions = list(periodos[::tick_step])
    tick_labels = list(etiquetas[::tick_step])

    if tick_positions[-1] != periodos[-1]:
        tick_positions.append(periodos[-1])
        tick_labels.append(etiquetas[-1])

    return tick_positions, tick_labels


def render_caudal_chart(ax, dataset: dict[str, Any]) -> None:
    meta = dataset["meta"]
    caudal = dataset["caudal"]

    q_opt = list(caudal["q_opt"])
    q_entrada_cincel = list(caudal["q_entrada_cincel"])
    q_referencia = float(caudal["q_referencia"])
    q_rango_min = float(caudal["q_rango_min"])
    q_rango_max = float(caudal["q_rango_max"])

    periodos = list(meta["periodos"])
    etiquetas = list(meta["horas_etiquetas"])
    tick_step = int(meta["tick_step"])
    titulo_modo = str(meta["titulo_modo"])

    if not q_opt or not q_entrada_cincel or not periodos:
        ax.text(
            0.5,
            0.5,
            "No hay datos suficientes para mostrar el gráfico.",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        return

    y_values = q_opt + q_entrada_cincel + [q_referencia, q_rango_min, q_rango_max]
    y_min = min(y_values)
    y_max = max(y_values)
    y_padding = max((y_max - y_min) * 0.08, 0.5)

    ax.fill_between(
        periodos,
        q_rango_min,
        q_rango_max,
        color="gray",
        alpha=0.15,
        label="Límites operativos",
    )
    ax.plot(
        periodos,
        q_opt,
        color="tab:blue",
        linewidth=2.2,
        label="Q optimizado",
    )
    ax.plot(
        periodos,
        q_entrada_cincel,
        color="darkgreen",
        linestyle="--",
        linewidth=1,
        alpha=0.5,
        label="Q entrada D. Cincel",
    )
    ax.axhline(
        y=q_referencia,
        color="r",
        linestyle="--",
        alpha=0.5,
        label=f"Promedio: {q_referencia:.1f} m3/s",
    )

    ax.set_title(
        f"Caudal Salida D. Cincel — {titulo_modo} (Q_Camp={q_referencia:.1f} m3/s)"
    )
    ax.set_xlabel("Periodo (30 min)")
    ax.set_ylabel("Caudal (m3/s)")
    ax.set_xlim(0.5, len(periodos) + 0.5)
    ax.set_ylim(y_min - y_padding, y_max + y_padding)

    tick_positions, tick_labels = _build_tick_positions_and_labels(
        periodos=periodos,
        etiquetas=etiquetas,
        tick_step=tick_step,
    )
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right")

    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")

def render_volumenes_chart(ax, dataset: dict[str, Any]) -> None:
    meta = dataset["meta"]
    volumenes = dataset["volumenes"]

    v_cincel = list(volumenes["v_cincel"])
    v_campanario = list(volumenes["v_campanario"])

    v_cincel_min = float(volumenes["v_cincel_min"])
    v_cincel_max = float(volumenes["v_cincel_max"])
    v_camp_min = float(volumenes["v_campanario_min"])
    v_camp_max = float(volumenes["v_campanario_max"])

    periodos = list(meta["periodos"])
    etiquetas = list(meta["horas_etiquetas"])
    tick_step = int(meta["tick_step"])
    titulo_modo = str(meta["titulo_modo"])

    if not v_cincel or not v_campanario or not periodos:
        ax.text(
            0.5,
            0.5,
            "No hay datos suficientes para mostrar el gráfico.",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        return

    y_values = (
        v_cincel
        + v_campanario
        + [v_cincel_min, v_cincel_max, v_camp_min, v_camp_max]
    )
    y_min = min(y_values)
    y_max = max(y_values)
    y_padding = max((y_max - y_min) * 0.05, 1000.0)

    ax.plot(
        periodos,
        v_cincel,
        color="tab:blue",
        linewidth=2.2,
        label="Vol. D. Cincel",
    )
    ax.plot(
        periodos,
        v_campanario,
        color="tab:green",
        linewidth=2.2,
        label="Vol. D. Campanario",
    )

    ax.fill_between(
        periodos,
        v_cincel_min,
        v_cincel_max,
        color="blue",
        alpha=0.07,
    )
    ax.fill_between(
        periodos,
        v_camp_min,
        v_camp_max,
        color="green",
        alpha=0.07,
    )

    ax.axhline(
        y=v_cincel_max,
        color="navy",
        linestyle=":",
        linewidth=1,
        alpha=0.5,
    )
    ax.axhline(
        y=v_cincel_min,
        color="navy",
        linestyle=":",
        linewidth=1,
        alpha=0.5,
    )
    ax.axhline(
        y=v_camp_max,
        color="darkgreen",
        linestyle=":",
        linewidth=1,
        alpha=0.5,
    )
    ax.axhline(
        y=v_camp_min,
        color="darkgreen",
        linestyle=":",
        linewidth=1,
        alpha=0.5,
    )

    ax.set_title(f"Evolución de Volúmenes — {titulo_modo}")
    ax.set_xlabel("Periodo (30 minutos)")
    ax.set_ylabel("Volumen (m3)")
    ax.set_xlim(0.5, len(periodos) + 0.5)
    ax.set_ylim(y_min - y_padding, y_max + y_padding)

    tick_positions, tick_labels = _build_tick_positions_and_labels(
        periodos=periodos,
        etiquetas=etiquetas,
        tick_step=tick_step,
    )
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right")

    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")

def render_despacho_chart(ax, dataset: dict[str, Any]) -> None:
    meta = dataset["meta"]
    despacho = dataset["despacho"]

    cmg = list(despacho["cmg"])
    potencia_ch4 = list(despacho["potencia_ch4"])
    potencia_ch6 = list(despacho["potencia_ch6"])
    correlacion = float(despacho.get("correlacion", 0.0))

    periodos = list(meta["periodos"])
    etiquetas = list(meta["horas_etiquetas"])
    tick_step = int(meta["tick_step"])
    titulo_modo = str(meta["titulo_modo"])

    if not cmg or not potencia_ch4 or not potencia_ch6 or not periodos:
        ax.text(
            0.5,
            0.5,
            "No hay datos suficientes para mostrar el gráfico.",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        return

    ax2 = ax.twinx()

    ax.plot(
        periodos,
        cmg,
        color="tab:red",
        linewidth=2,
        label="CMG",
        alpha=0.9,
    )
    ax.fill_between(periodos, 0, cmg, color="red", alpha=0.08)

    ax2.plot(
        periodos,
        potencia_ch4,
        color="tab:blue",
        linewidth=2,
        label="Charcani 4",
        alpha=0.9,
    )
    ax2.plot(
        periodos,
        potencia_ch6,
        color="tab:green",
        linewidth=2,
        linestyle="--",
        label="Charcani 6",
        alpha=0.9,
    )

    ax.set_title(f"Despacho Económico — {titulo_modo} (Corr: {correlacion:.3f})")
    ax.set_xlabel("Periodo (30 min)")
    ax.set_ylabel("CMG (S/./MWh)", color="r")
    ax2.set_ylabel("Potencia (MW)", color="b")

    ax.tick_params(axis="y", labelcolor="r")
    ax2.tick_params(axis="y", labelcolor="b")

    ax.set_xlim(0.5, len(periodos) + 0.5)

    tick_positions, tick_labels = _build_tick_positions_and_labels(
        periodos=periodos,
        etiquetas=etiquetas,
        tick_step=tick_step,
    )
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right")

    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")