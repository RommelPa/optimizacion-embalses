# Guía del Motor PSO

## Objetivo

Este documento describe cómo está modularizado actualmente el motor PSO dentro del proyecto, indicando qué archivo contiene cada parte del flujo y qué nivel de impacto tiene cada cambio.

El objetivo es que cualquier ingeniero pueda identificar rápidamente:

- dónde se valida la entrada,
- dónde se transforma el Excel al contrato interno,
- dónde corre el PSO,
- dónde está la función objetivo,
- dónde se calcula la simulación hidráulica,
- dónde se arma la salida para la aplicación.

## Flujo técnico resumido

```text
CorridaService
  -> ejecutar_corrida_pso
  -> build_engine_input_from_wrapper
  -> build_engine_input_from_excel
  -> run_pso_engine
      -> ejecutar_optimizacion_pso
      -> reparar_solucion_inteligente
      -> calcular_volumenes_con_caudales
```

## Vista general del flujo

El flujo actual del PSO es este:

1. La aplicación desktop crea una corrida.
2. `CorridaService` arma un `PSOWrapperInput`.
3. El wrapper PSO transforma ese input a un `EngineInputContract`.
4. Si el origen es Excel, se lee y valida el archivo.
5. El engine ejecuta la optimización PSO.
6. Se calculan series de salida y métricas.
7. El resultado se persiste en base de datos.
8. La corrida puede verse en detalle o exportarse a Excel.

## Nivel de impacto de cambios

### Impacto bajo
- `wrapper.py`
- `contracts.py`
- `errors.py`

### Impacto medio
- `input_mapper.py`
- `engine_runner.py`

### Impacto alto
- `excel_reader.py`
- `engine_input_contract.py`
- `config.py`

### Impacto muy alto
- `optimizer.py`
- `objective.py`
- `repair.py`
- `simulation.py`

## Mapa de archivos del motor PSO

## 1. `wrapper.py`

**Ruta:** `backend/app/integrations/pso/wrapper.py`  
**Responsabilidad:** puerta de entrada al motor PSO desde la capa de aplicación.

### Qué hace
- recibe `PSOWrapperInput`,
- construye el input interno del motor,
- llama al runner del engine,
- traduce el resultado del engine a `PSOWrapperOutput`,
- encapsula errores de ejecución como `PSOExecutionError`.

### Cuándo tocarlo
Tócalo si necesitas:
- cambiar el contrato externo del wrapper,
- cambiar cómo se arma la salida del motor,
- interceptar o traducir errores del engine.

### Cuándo no tocarlo
No lo toques para modificar la lógica matemática del PSO.

---

## 2. `contracts.py`

**Ruta:** `backend/app/integrations/pso/contracts.py`  
**Responsabilidad:** definir los modelos de entrada y salida del wrapper.

### Modelos principales
- `PSOWrapperInput`
- `PSOWrapperOutput`

### Qué contiene
- metadatos de corrida,
- modo de operación,
- origen de datos,
- archivo de entrada,
- salida estructurada del motor.

### Cuándo tocarlo
Tócalo si cambia el contrato entre aplicación y motor.

---

## 3. `input_mapper.py`

**Ruta:** `backend/app/integrations/pso/input_mapper.py`  
**Responsabilidad:** convertir `PSOWrapperInput` en `EngineInputContract`.

### Qué hace
- valida que la V1 solo use:
  - `modo_operacion = inicial`
  - `origen_datos = excel`
- delega la construcción real al lector Excel.

### Cuándo tocarlo
Tócalo si:
- cambia el alcance de V1,
- entra un nuevo origen de datos,
- se habilita reprogramación,
- cambia la forma de construir el input del motor.

### Riesgo
Es una pieza sensible porque conecta reglas funcionales de producto con el motor.

---

## 4. `engine_input_contract.py`

**Ruta:** `backend/app/integrations/pso/engine_input_contract.py`  
**Responsabilidad:** definir el contrato validado que consume el motor PSO.

### Modelos principales
- `SeriesInput`
- `RestriccionesInput`
- `ConfiguracionPSOInput`
- `EngineInputContract`

### Qué valida
- series no vacías,
- longitudes consistentes,
- número de periodos esperado,
- coherencia de restricciones,
- límites y rangos básicos.

### Cuándo tocarlo
Tócalo si:
- cambian las reglas del dominio,
- cambia la cantidad de periodos,
- cambian parámetros físicos o restricciones del motor.

### Riesgo
Muy alto. Si se debilita este contrato, el engine empieza a recibir basura bien formada.

---

## 5. `excel_reader.py`

**Ruta:** `backend/app/integrations/pso/excel_reader.py`  
**Responsabilidad:** leer el archivo Excel de entrada y construir el `EngineInputContract`.

### Qué hace
- verifica que el archivo exista,
- lee el Excel,
- valida columnas obligatorias,
- valida registros mínimos y requeridos,
- convierte series a numérico,
- lee `q_salida_campanario`,
- construye `SeriesInput`, `RestriccionesInput` y `ConfiguracionPSOInput`.

### Qué columnas usa actualmente
- `CMG`
- `P_CHAR 5`

### Qué valor escalar usa actualmente
- `Q_SALIDA_CAMPANARIO` desde la estructura definida por la plantilla V1.

### Cuándo tocarlo
Tócalo si:
- cambia la plantilla Excel,
- cambian nombres de columnas,
- cambian parámetros requeridos,
- se agregan nuevas validaciones de entrada.

### Riesgo
Muy alto. Es el contrato operativo del sistema.

---

## 6. `config.py`

**Ruta:** `backend/app/integrations/pso/config.py`  
**Responsabilidad:** definir valores por defecto y constantes base del motor.

### Qué contiene
- límites de volúmenes,
- rango de caudales,
- rendimientos,
- parámetros por defecto del PSO,
- factores de volumen inicial y final.

### Importante
La configuración operativa efectiva del sistema ya no depende solo de este archivo.  
Actualmente existe configuración persistida en base de datos, y cada corrida guarda un snapshot de la configuración usada.

### Cuándo tocarlo
Tócalo si:
- cambian defaults del sistema,
- cambian constantes base del modelo,
- necesitas redefinir valores por defecto iniciales.

### Riesgo
Alto. Cambiar defaults aquí impacta el comportamiento base del motor y la inicialización de nuevas configuraciones.

---

## 7. `engine_runner.py`

**Ruta:** `backend/app/integrations/pso/engine/engine_runner.py`  
**Responsabilidad:** orquestar la ejecución del engine PSO.

### Qué hace
- llama al optimizador PSO,
- toma `q_opt`,
- ejecuta simulación con caudales optimizados,
- calcula:
  - volúmenes,
  - potencias,
  - ingresos,
  - series de salida,
- devuelve un resultado consolidado.

### Cuándo tocarlo
Tócalo si:
- cambias el flujo general de ejecución,
- agregas nuevas salidas derivadas,
- cambias el postprocesamiento después del optimizador.

### Cuándo no tocarlo
No lo toques para ajustar penalidades o estrategia de reparación. Eso va en otros módulos.

---

## 8. `optimizer.py`

**Ruta:** `backend/app/integrations/pso/engine/optimizer.py`  
**Responsabilidad:** implementar la ejecución iterativa del algoritmo PSO.

### Qué hace
- construye posiciones iniciales,
- configura el optimizador `GlobalBestPSO`,
- ejecuta iteraciones,
- aplica inercia dinámica,
- guarda la mejor solución encontrada,
- aplica reparación final,
- devuelve:
  - `best_cost`
  - `q_opt`
  - `execution_time_sec`
  - historial de costo

### Cuándo tocarlo
Tócalo si quieres modificar:
- número de partículas,
- iteraciones,
- construcción de posiciones iniciales,
- política de inercia,
- control del ciclo de optimización.

### Riesgo
Alto. Aquí cambias comportamiento del algoritmo, no solo estructura.

---

## 9. `objective.py`

**Ruta:** `backend/app/integrations/pso/engine/objective.py`  
**Responsabilidad:** definir la función objetivo que el PSO minimiza.

### Qué hace
Para cada partícula:
- repara la solución propuesta,
- simula volúmenes,
- calcula potencias,
- calcula ingresos,
- aplica penalizaciones por:
  - sobrepasar máximos,
  - bajar de mínimos,
  - volumen negativo,
  - desviación del volumen final,
  - falta de suavidad.

### Cuándo tocarlo
Tócalo si quieres modificar:
- lógica económica,
- penalidades,
- pesos relativos de restricciones,
- criterio de costo total.

### Riesgo
Muy alto. Este archivo cambia el comportamiento central del modelo.

---

## 10. `repair.py`

**Ruta:** `backend/app/integrations/pso/engine/repair.py`  
**Responsabilidad:** corregir soluciones propuestas por el PSO para acercarlas a restricciones válidas.

### Qué hace
- suaviza el caudal propuesto,
- lo recorta a rango operativo,
- simula volúmenes,
- detecta violaciones,
- ajusta iterativamente,
- corrige error final de volumen,
- devuelve un `q_final` suavizado y acotado.

### Cuándo tocarlo
Tócalo si:
- cambias la lógica de reparación,
- cambias el suavizado,
- cambias los ajustes por exceso o déficit,
- cambias la corrección final del volumen.

### Riesgo
Muy alto. Este módulo afecta fuertemente estabilidad y validez de soluciones.

---

## 11. `simulation.py`

**Ruta:** `backend/app/integrations/pso/engine/simulation.py`  
**Responsabilidad:** simular evolución de volúmenes y detectar violaciones.

### Funciones principales
- `calcular_volumenes_con_caudales`
- `verificar_violaciones`

### Qué hace
- calcula volúmenes de Cincel y Campanario por periodo,
- calcula `q_ch4` y `q_ch6`,
- verifica:
  - sobre máximos,
  - bajo mínimos,
  - excesos acumulados,
  - déficits acumulados,
  - volúmenes negativos.

### Cuándo tocarlo
Tócalo si cambian:
- ecuaciones de simulación,
- desfase hidráulico,
- forma de contabilizar violaciones.

### Riesgo
Muy alto. Esta es la base física del resultado.

---

## 12. `errors.py`

**Ruta:** `backend/app/integrations/pso/errors.py`  
**Responsabilidad:** definir excepciones propias del wrapper PSO.

### Excepciones
- `PSOWrapperError`
- `PSOValidationError`
- `PSOExecutionError`

### Qué significan
- `PSOValidationError`: entrada inválida o contrato incorrecto
- `PSOExecutionError`: error técnico durante la ejecución del motor

### Uso recomendado
- usar `PSOValidationError` para rechazar entrada,
- usar `PSOExecutionError` para fallas técnicas del engine.

## Relación con la capa de aplicación

## `corrida_service.py`

**Ruta:** `backend/app/application/corrida_service.py`  
**Responsabilidad respecto al PSO:**
- arma `PSOWrapperInput`,
- llama `ejecutar_corrida_pso`,
- persiste resultados,
- clasifica estados:
  - `completada`
  - `rechazada`
  - `fallida`

### Importante
El que trabaje el algoritmo no debería empezar por aquí, salvo que también quiera modificar:
- cómo se persisten resultados,
- cómo se traducen errores,
- cómo se expone la corrida al resto del sistema.

## Qué archivo tocar según el tipo de cambio

### Si quieres cambiar validación del archivo Excel
- `excel_reader.py`
- `engine_input_contract.py`

### Si quieres cambiar parámetros globales del modelo
- `config.py`

### Si quieres cambiar cómo entra el input al motor
- `input_mapper.py`
- `contracts.py`
- `engine_input_contract.py`

### Si quieres cambiar cómo se inicializa el PSO
- `optimizer.py`

### Si quieres cambiar cómo se calcula el costo total
- `objective.py`

### Si quieres cambiar cómo se reparan soluciones
- `repair.py`

### Si quieres cambiar cómo se simulan volúmenes y restricciones
- `simulation.py`

### Si quieres cambiar cómo se arma la salida del motor
- `engine_runner.py`
- `wrapper.py`

## Orden recomendado para intervenir el algoritmo

Si el objetivo es modificar comportamiento del modelo, el orden recomendado es:

1. leer `config.py`
2. leer `engine_input_contract.py`
3. leer `excel_reader.py`
4. leer `engine_runner.py`
5. leer `simulation.py`
6. leer `repair.py`
7. leer `objective.py`
8. leer `optimizer.py`

Ese orden permite entender:
- entrada,
- restricciones,
- simulación,
- reparación,
- costo,
- optimización.

No al revés.

## Qué no tocar primero

No conviene empezar por:

- `wrapper.py`
- `corrida_service.py`
- `excel_exporter.py`
- UI desktop

si el objetivo es trabajar el algoritmo.

Eso es periferia del sistema, no núcleo matemático.

## Riesgos actuales conocidos

- Las tolerancias numéricas contra benchmark legacy aún no están formalizadas.
- Los umbrales de aceptación del resultado aún no están cerrados.
- La V1 está cerrada a `inicial + excel`; reprogramación y carga manual quedan fuera por ahora.

## Recomendación de trabajo

Si el objetivo es mejorar o validar el algoritmo sin romper el sistema:

1. no cambiar la interfaz del wrapper sin coordinación,
2. no cambiar el contrato Excel sin actualizar documentación,
3. no tocar UI ni persistencia mientras se trabaja el modelo,
4. trabajar primero dentro de:
   - `config.py`
   - `simulation.py`
   - `repair.py`
   - `objective.py`
   - `optimizer.py`

## Estado técnico actual del motor

El motor PSO ya está modularizado en piezas separadas y funcionales.

Queda pendiente cerrar técnicamente:

- benchmark contra legacy,
- tolerancias numéricas,
- umbrales de aceptación,
- contrato final de la plantilla Excel.
