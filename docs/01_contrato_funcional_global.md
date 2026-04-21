# Contrato Funcional Global del Producto

## Objetivo

Definir el comportamiento funcional del sistema en su estado actual y en sus siguientes versiones, separando claramente qué pertenece a la base operativa y qué entra en la evolución posterior.

## 1. Flujo base operativo actual (V1.0)

### Entrada soportada
- archivo Excel oficial,
- modo de operación `inicial`.

### Flujo
1. El usuario abre la app desktop.
2. Crea una nueva corrida.
3. Ingresa metadatos mínimos.
4. Selecciona archivo Excel.
5. El sistema valida la entrada.
6. Si la entrada es válida, ejecuta el motor PSO.
7. Guarda la corrida en persistencia local.
8. Permite revisar historial, detalle y exportación.

### Salidas principales
- resultado resumido,
- detalle de corrida,
- exportación Excel,
- historial local.

## 2. Flujo previsto para V1.1 — Interfaz Windows

La V1.1 no cambia el contrato principal de negocio. Cambia la experiencia de uso:

- menús superiores,
- toolbar,
- navegación más clásica,
- acciones agrupadas en menús tipo Archivo / Corridas / Configuración / Ayuda,
- controles visuales más familiares para operadores.

## 3. Flujo previsto para V1.2 — Acceso y perfiles

### Autenticación
El sistema exigirá inicio de sesión.

### Perfiles
- Operador
- Ingeniero / Programador

### Diferencia funcional
- el Operador ejecuta corridas y ve parámetros permitidos,
- el Ingeniero / Programador además puede editar configuración del sistema.

## 4. Flujo previsto para V1.3 — Configuración editable

### Configuración global
El sistema tendrá configuración persistente, editable desde UI, sin tocar el código.

Parámetros previstos:
- configuración PSO,
- parámetros del modelo,
- restricciones operativas visibles o editables según perfil.

### Trazabilidad
Cada corrida deberá guardar la configuración usada.

## 5. Flujo previsto para V1.4 — Carga manual y gestión de corridas

### Carga manual
Se habilitará entrada manual del sistema, pero usando el mismo contrato interno del motor.

Eso significa que:
- Excel y manual deben producir el mismo `EngineInputContract`,
- la carga manual no debe crear un flujo paralelo inconsistente.

### Gestión de corridas
Se agregará:
- comparación entre corridas,
- favoritos / casos base,
- borrado automático mensual.

## 6. Flujo previsto para V1.5 — Validación y reprogramación

### Validación del modelo
- benchmark contra legacy,
- definición de tolerancias,
- criterios de aceptación.

### Reprogramación
- definición funcional,
- adaptación del flujo,
- pruebas y validación.

## 7. Flujo previsto para V1.6 — Integraciones y despliegue

### Integraciones
- scraping COES,
- alertas.

### Despliegue
- empaquetado,
- instalador Windows,
- distribución manual,
- actualización manual,
- posible evaluación de infraestructura adicional.

## 8. Reglas funcionales transversales

- cada corrida debe registrar qué configuración se usó,
- los errores deben ser claros y trazables,
- las validaciones deben ocurrir antes del cálculo cuando sea posible,
- el sistema no debe exponer opciones no soportadas por la versión actual,
- toda nueva versión debe quedar documentada antes de abrir más alcance.

## 9. Estados funcionales de corrida

Estados mínimos actuales:
- `completada`
- `rechazada`
- `fallida`

Estados futuros posibles:
- `validando`
- `ejecutando`

## 10. Fuera del alcance inmediato

No forman parte de la base operativa actual:
- centralización obligatoria en servidor,
- despliegue web del producto principal,
- automatización total de distribución,
- administración avanzada de usuarios.
