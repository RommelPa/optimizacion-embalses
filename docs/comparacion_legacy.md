# Comparación final contra legacy

## Objetivo

Dejar trazado el estado real de equivalencia entre la implementación modular actual y el script legacy original de optimización PSO para Charcani 4 y 6.

## Estado actual

La implementación nueva ya replica de forma muy cercana la estructura, reportería y gran parte del comportamiento matemático del legacy. Sin embargo, todavía no debe afirmarse equivalencia exacta absoluta contra cualquier archivo histórico legacy si ese archivo fue generado sin una semilla aleatoria controlada.

## Lo que ya quedó alineado

### Insumos

* lectura de `CMG`
* lectura de `P_CHAR 5`
* cálculo de `Q_Cincel = P_CHAR 5 / 5.98`
* lectura de `Q_salida_Campanario`
* uso de 48 períodos en modo programa inicial
* parámetros hidráulicos y límites de embalses

### Núcleo del modelo

* simulación de volúmenes de Dique Cincel y Dique Campanario
* desfase hidráulico entre salida de Cincel y toma en Campanario
* reparación inteligente de soluciones
* función objetivo con penalizaciones fuertes
* optimización PSO con inercia dinámica
* cálculo de potencias CH4 y CH6
* cálculo de ingresos por período

### Configuración PSO ya corregida

* `n_particles = 150`
* `max_iter = 150`
* `c1 = 2.0`
* `c2 = 2.0`
* `w` dinámica desde `0.9` hasta `0.4`
* `v_max = 1.5`
* semilla fija para validación reproducible en la implementación nueva

### Persistencia y trazabilidad

* guardado de `q_salida_campanario`
* guardado de `p_char_5`
* guardado de series resultantes
* exportación JSON
* exportación CSV
* exportación Excel legacy-compatible

### Excel legacy-compatible

* una sola hoja `Resultados`
* columnas equivalentes al legacy
* bloque de resumen debajo de la tabla
* 3 gráficos incrustados en la misma hoja
* nombre de archivo coherente con el formato del legacy

## Lo que ya puede considerarse equivalente

* estructura general del archivo Excel
* columnas principales de entrada y salida
* uso de datos reales del archivo de entrada
* lógica hidráulica base
* reportería visual equivalente en intención funcional

## Lo que todavía no puede afirmarse como cerrado al 100%

* igualdad numérica exacta contra cualquier archivo legacy histórico ya generado
* coincidencia exacta de ingresos y caudales período a período frente a un archivo legacy sin semilla conocida
* igualdad exacta de `Tiempo total` frente al script original
* equivalencia absoluta de cualquier corrida histórica generada con estado aleatorio no controlado

## Causa principal de la diferencia residual

El script legacy original no fija semilla aleatoria de forma explícita en el bloque de optimización. Por eso, un archivo legacy histórico puede corresponder a una trayectoria estocástica que no puede reconstruirse exactamente solo con el código.

En la implementación nueva se fijó semilla para lograr reproducibilidad y permitir validación controlada.

## Interpretación correcta

No debe compararse una implementación reproducible con un archivo histórico legacy generado bajo aleatoriedad no controlada como si ambos debieran coincidir exactamente en todos los valores.

La comparación correcta debe ser una de estas dos:

1. equivalencia funcional y estructural suficiente
2. equivalencia exacta reproducible usando la misma semilla en legacy y en la implementación nueva

## Recomendación técnica

Para una validación dura y trazable, el camino correcto es:

1. fijar semilla también en el script legacy
2. generar una nueva corrida legacy controlada
3. comparar esa nueva salida contra la implementación modular actual

## Checklist de equivalencia

### Ya resuelto

* [x] lectura de `CMG`
* [x] lectura de `P_CHAR 5`
* [x] lectura de `Q_salida_Campanario`
* [x] construcción de `Q_Cincel`
* [x] simulación de volúmenes
* [x] reparación inteligente
* [x] función objetivo con penalizaciones
* [x] configuración PSO alineada con el legacy
* [x] persistencia de series clave
* [x] hoja `Resultados`
* [x] columnas legacy
* [x] bloque de resumen
* [x] gráficos incrustados en Excel

### Pendiente por decisión

* [ ] aceptar equivalencia funcional como suficiente
* [ ] exigir igualdad exacta reproducible con semilla fija también en legacy
* [ ] alinear exactamente `Tiempo total`
* [ ] decidir si la semilla quedará fija o configurable

## Conclusión

La implementación nueva ya no debe considerarse una aproximación superficial. El sistema actual replica gran parte del flujo legacy, tanto en cálculo como en reportería. La brecha restante ya no es principalmente estructural, sino de reproducibilidad exacta y criterio de validación.

El siguiente trabajo de producto puede continuar siempre que quede claro si el proyecto exige:

* equivalencia funcional suficiente
* o equivalencia exacta reproducible con semilla controlada
