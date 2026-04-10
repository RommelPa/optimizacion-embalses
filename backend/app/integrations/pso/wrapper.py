import numpy as np

from app.integrations.pso.contracts import PSOWrapperInput, PSOWrapperOutput
from app.integrations.pso.engine.engine_runner import run_pso_engine
from app.integrations.pso.errors import PSOExecutionError, PSOValidationError
from app.integrations.pso.input_mapper import build_engine_input_from_wrapper


def ejecutar_corrida_pso(payload: PSOWrapperInput) -> PSOWrapperOutput:
    try:
        engine_input = build_engine_input_from_wrapper(payload)

        resultado = run_pso_engine(
            horas=engine_input.horas,
            q_rango=(
                engine_input.restricciones.q_rango_min,
                engine_input.restricciones.q_rango_max,
            ),
            q_cincel=np.array(engine_input.series.q_cincel, dtype=np.float64),
            q_salida_campanario=engine_input.restricciones.q_salida_campanario,
            v_cincel_inicio=engine_input.restricciones.v_cincel_inicio,
            v_campanario_inicio=engine_input.restricciones.v_campanario_inicio,
            v_cincel_final=engine_input.restricciones.v_cincel_final,
            v_campanario_final=engine_input.restricciones.v_campanario_final,
            v_cincel_max=engine_input.restricciones.v_cincel_max,
            v_cincel_min=engine_input.restricciones.v_cincel_min,
            v_campanario_max=engine_input.restricciones.v_campanario_max,
            v_campanario_min=engine_input.restricciones.v_campanario_min,
            rendimiento_ch4=engine_input.restricciones.rendimiento_ch4,
            rendimiento_ch6=engine_input.restricciones.rendimiento_ch6,
            costo_marginal=np.array(engine_input.series.costo_marginal, dtype=np.float64),
            n_particles=engine_input.configuracion_pso.n_particles,
            max_iter=engine_input.configuracion_pso.max_iter,
        )

        return PSOWrapperOutput(
            estado="completada",
            version_modelo="pso-engine-v1",
            modo_ejecucion="normal",
            mensaje_modelo=(
                f"Corrida ejecutada con motor PSO real controlado para escenario "
                f"'{payload.escenario}' y origen '{payload.origen_datos}'."
            ),
            best_cost=resultado["best_cost"],
            execution_time_sec=resultado["execution_time_sec"],
            q_opt=[float(x) for x in resultado["q_opt"]],
            v_cincel=[float(x) for x in resultado["v_cincel"]],
            v_campanario=[float(x) for x in resultado["v_campanario"]],
            cmg=[float(x) for x in resultado["cmg"]],
            potencia_ch4=[float(x) for x in resultado["potencia_ch4"]],
            potencia_ch6=[float(x) for x in resultado["potencia_ch6"]],
            ingreso=[float(x) for x in resultado["ingreso"]],
        )

    except PSOValidationError:
        raise
    except Exception as exc:
        raise PSOExecutionError(
            f"Error durante la ejecución del motor PSO: {exc}"
        ) from exc