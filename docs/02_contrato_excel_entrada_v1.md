# Contrato Excel de Entrada V1

## Objetivo

Definir la estructura oficial del Excel de entrada para la corrida base del sistema.

## Alcance

Este contrato aplica al flujo Excel de la base operativa actual y sirve como referencia hasta que la carga manual quede habilitada en una versión posterior.

## Estructura general

La plantilla oficial debe contener dos hojas:

1. `Series`
2. `Parametros`

## Hoja `Series`

Columnas obligatorias:

| Columna | Tipo esperado | Obligatoria | Descripción |
|---|---|---|---|
| `PERIODO` | entero | sí | índice de 1 a 48 |
| `HORA` | texto | sí | hora del periodo |
| `CMG` | numérico | sí | costo marginal |
| `P_CHAR 5` | numérico | sí | potencia Char 5 |

### Reglas
- deben existir 48 filas operativas,
- no se permiten vacíos en `CMG` ni `P_CHAR 5`,
- `CMG` debe ser convertible a número,
- `P_CHAR 5` debe ser convertible a número.

## Hoja `Parametros`

Parámetros previstos:

| Parámetro | Valor |
|---|---|
| `Q_SALIDA_CAMPANARIO` | número |
| `FECHA_PROCESO` | texto o fecha |
| `ESCENARIO` | texto |

### Parámetro obligatorio actual
- `Q_SALIDA_CAMPANARIO`

## Transformaciones derivadas

A partir de `P_CHAR 5`, el sistema calcula:

- `q_cincel = P_CHAR 5 / 5.98`

## Reglas de validación

El sistema debe rechazar el archivo si:
- falta la hoja `Series`,
- falta la hoja `Parametros`,
- faltan columnas obligatorias,
- faltan parámetros obligatorios,
- no existen 48 registros válidos,
- `CMG` contiene valores no numéricos,
- `P_CHAR 5` contiene valores no numéricos,
- `Q_SALIDA_CAMPANARIO` no es numérico,
- `Q_SALIDA_CAMPANARIO` es menor o igual a 0.

## Evolución esperada

En futuras versiones, el contrato Excel seguirá siendo relevante incluso si entra carga manual, porque Excel seguirá siendo una fuente oficial de entrada y validación operativa.
