# Perfiles y Configuración del Sistema

## Objetivo

Definir cómo funcionarán los perfiles de usuario y qué parámetros serán visibles o editables desde la aplicación.

## Perfiles

### Operador
Puede:
- iniciar sesión,
- crear corridas,
- usar flujo Excel,
- revisar historial,
- revisar detalle,
- exportar resultados,
- ver ciertos parámetros operativos.

No debería editar parámetros avanzados del algoritmo sin validación de negocio.

### Ingeniero / Programador
Puede:
- hacer todo lo del Operador,
- editar configuración global,
- cambiar parámetros del algoritmo,
- cambiar parámetros del modelo,
- cambiar restricciones operativas según se defina,
- restaurar valores por defecto,
- validar configuración usada por corrida.

## Parámetros previstos

### Parámetros del algoritmo
- `c1`
- `c2`
- `w`
- `v_max`
- `DEFAULT_N_PARTICLES`
- `DEFAULT_MAX_ITER`

### Parámetros del modelo
- `RENDIMIENTO_CH4`
- `RENDIMIENTO_CH6`
- `DEFAULT_V_INICIO_FACTOR`
- `DEFAULT_V_FINAL_FACTOR`

### Restricciones operativas
- `V_CINCEL_MAX`
- `V_CINCEL_MIN`
- `V_CAMPANARIO_MAX`
- `V_CAMPANARIO_MIN`
- `Q_RANGO_MIN`
- `Q_RANGO_MAX`

## Reglas acordadas

- todos esos parámetros serán configurables desde el sistema en versiones posteriores,
- la configuración será global,
- debe existir opción para restaurar valores por defecto,
- cada corrida deberá guardar snapshot de configuración,
- los perfiles podrán ver o editar según permisos definidos.

## Persistencia futura esperada

La configuración no debe vivir solo en constantes del código. Debe persistirse localmente para:
- reutilización,
- trazabilidad,
- auditoría,
- reproducción de corridas.

## Trazabilidad obligatoria por corrida

Cada corrida deberá guardar:
- usuario que la ejecutó,
- perfil,
- parámetros de configuración usados,
- restricciones usadas,
- fecha y hora,
- resultado y estado.

## Carga manual

La carga manual se incorpora en una versión posterior.

Cuando entre, deberá:
- usar validaciones fuertes,
- respetar perfiles,
- construir el mismo contrato interno que el flujo Excel.
