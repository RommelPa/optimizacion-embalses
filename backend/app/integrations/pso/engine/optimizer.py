import time

import numpy as np
import pyswarms as ps

from app.integrations.pso.engine.objective import funcion_objetivo_unificada
from app.integrations.pso.engine.repair import reparar_solucion_inteligente

np.random.seed(42)


def construir_posiciones_iniciales(
    horas: int,
    n_particles: int,
    q_salida_campanario: float,
    q_cincel: np.ndarray,
    q_rango: tuple[float, float],
) -> np.ndarray:
    q_inicial_base = np.full(horas, q_salida_campanario, dtype=np.float64)

    for t in range(horas):
        if q_cincel[t] > q_salida_campanario + 2.0:
            q_inicial_base[t] = min(q_inicial_base[t] + 0.8, q_rango[1] - 0.5)
        elif q_cincel[t] < q_salida_campanario - 2.0:
            q_inicial_base[t] = max(q_inicial_base[t] - 0.8, q_rango[0] + 0.5)

    init_pos = np.tile(q_inicial_base, (n_particles, 1))
    for i in range(n_particles):
        noise = np.random.randn(horas) * 0.4
        init_pos[i] = np.clip(init_pos[i] + noise, q_rango[0], q_rango[1])

    return init_pos.astype(np.float64)


def ejecutar_optimizacion_pso(
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
    n_particles: int = 150,
    max_iter: int = 150,
    c1: float = 2.0,
    c2: float = 2.0,
    w: float = 0.9,
    v_max: float = 1.5,
) -> dict:
    init_pos = construir_posiciones_iniciales(
        horas=horas,
        n_particles=n_particles,
        q_salida_campanario=q_salida_campanario,
        q_cincel=q_cincel,
        q_rango=q_rango,
    )

    options = {
        "c1": float(c1),
        "c2": float(c2),
        "w": float(w),
    }

    optimizador = ps.single.GlobalBestPSO(
        n_particles=n_particles,
        dimensions=horas,
        options=options,
        bounds=(
            np.array([q_rango[0]] * horas, dtype=np.float64),
            np.array([q_rango[1]] * horas, dtype=np.float64),
        ),
        velocity_clamp=(-float(v_max), float(v_max)),
        init_pos=init_pos,
    )

    w_inicial = float(w)
    w_final = max(0.3, float(w) * 0.5)

    best_cost: float | None = None
    best_pos: np.ndarray | None = None
    cost_history: list[float] = []

    tiempo_inicio = time.time()

    for iteracion in range(max_iter):
        divisor = max(1, max_iter)
        w_actual = w_final + (w_inicial - w_final) * (1 - iteracion / divisor)
        optimizador.options["w"] = float(w_actual)

        try:
            cost, pos = optimizador.optimize(
                lambda positions: funcion_objetivo_unificada(
                    positions=positions,
                    horas=horas,
                    q_rango=q_rango,
                    q_cincel=q_cincel,
                    q_salida_campanario=q_salida_campanario,
                    v_cincel_inicio=v_cincel_inicio,
                    v_campanario_inicio=v_campanario_inicio,
                    v_cincel_final=v_cincel_final,
                    v_campanario_final=v_campanario_final,
                    v_cincel_max=v_cincel_max,
                    v_cincel_min=v_cincel_min,
                    v_campanario_max=v_campanario_max,
                    v_campanario_min=v_campanario_min,
                    rendimiento_ch4=rendimiento_ch4,
                    rendimiento_ch6=rendimiento_ch6,
                    costo_marginal=costo_marginal,
                ),
                iters=1,
                verbose=False,
            )
            cost = float(cost)
            pos = np.asarray(pos, dtype=np.float64)
        except Exception as exc:
            if best_pos is not None and best_cost is not None:
                pos = best_pos.copy()
                cost = best_cost
            else:
                raise RuntimeError(f"Error en optimizacion PSO: {exc}") from exc

        cost_history.append(float(cost))

        if best_cost is None or cost < best_cost:
            best_cost = float(cost)
            best_pos = pos.copy()

    if best_pos is None or best_cost is None:
        raise RuntimeError("La optimización PSO no produjo una solución válida.")

    q_opt = reparar_solucion_inteligente(
        q_prop=best_pos,
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

    tiempo_total = time.time() - tiempo_inicio

    return {
        "best_cost": float(best_cost),
        "q_opt": q_opt,
        "cost_history": cost_history,
        "execution_time_sec": round(tiempo_total, 4),
        "n_particles": n_particles,
        "max_iter": max_iter,
        "c1": float(c1),
        "c2": float(c2),
        "w": float(w),
        "v_max": float(v_max),
    }