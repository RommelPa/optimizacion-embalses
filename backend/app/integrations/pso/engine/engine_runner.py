from app.integrations.pso.engine.optimizer import ejecutar_optimizacion_pso


def run_pso_engine(
    horas: int,
    q_rango: tuple[float, float],
    q_cincel,
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
    costo_marginal,
    n_particles: int = 30,
    max_iter: int = 20,
):
    resultado = ejecutar_optimizacion_pso(
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
        n_particles=n_particles,
        max_iter=max_iter,
    )

    return {
        "engine": "pso",
        "status": "success",
        "best_cost": resultado["best_cost"],
        "q_opt": resultado["q_opt"],
        "execution_time_sec": resultado["execution_time_sec"],
        "n_particles": resultado["n_particles"],
        "max_iter": resultado["max_iter"],
        "cost_history": resultado["cost_history"],
    }