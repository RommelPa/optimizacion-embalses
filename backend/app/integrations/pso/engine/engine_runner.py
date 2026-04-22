from app.integrations.pso.engine.optimizer import ejecutar_optimizacion_pso
from app.integrations.pso.engine.simulation import calcular_volumenes_con_caudales


def run_pso_engine(
    horas: int,
    q_rango: tuple[float, float],
    q_cincel,
    q_salida_campanario: float,
    p_char_5,
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
    c1: float = 2.0,
    c2: float = 2.0,
    w: float = 0.9,
    v_max: float = 1.5,
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
        c1=c1,
        c2=c2,
        w=w,
        v_max=v_max,
    )

    q_opt = resultado["q_opt"]

    v_cincel, v_campanario, q_ch4, q_ch6 = calcular_volumenes_con_caudales(
        q_salida_cincel=q_opt,
        horas=horas,
        v_cincel_inicio=v_cincel_inicio,
        v_campanario_inicio=v_campanario_inicio,
        q_cincel=q_cincel,
        q_salida_campanario=q_salida_campanario,
    )

    potencia_ch4 = rendimiento_ch4 * q_ch4
    potencia_ch6 = rendimiento_ch6 * q_ch6
    ingreso = 0.5 * (potencia_ch4 + potencia_ch6) * costo_marginal

    return {
        "engine": "pso",
        "status": "success",
        "best_cost": resultado["best_cost"],
        "q_opt": resultado["q_opt"],
        "execution_time_sec": resultado["execution_time_sec"],
        "v_cincel": v_cincel,
        "v_campanario": v_campanario,
        "cmg": costo_marginal,
        "potencia_ch4": potencia_ch4,
        "potencia_ch6": potencia_ch6,
        "ingreso": ingreso,
        "q_salida_campanario": float(q_salida_campanario),
        "p_char_5": p_char_5.tolist() if hasattr(p_char_5, "tolist") else list(p_char_5),
        "n_particles": resultado["n_particles"],
        "max_iter": resultado["max_iter"],
        "cost_history": resultado["cost_history"],
    }