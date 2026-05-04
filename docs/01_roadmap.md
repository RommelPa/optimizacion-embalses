# Roadmap del Producto

## Propósito del producto

Optimización de Embalses es una aplicación de escritorio Windows para operadores e ingenieros del centro de control, diseñada para ejecutar corridas de optimización PSO de forma trazable, validada y operativamente usable, sin depender de manipulación directa del código.

El producto busca reemplazar el flujo legacy operativo por una aplicación de escritorio con interfaz familiar, persistencia local y exportación controlada de resultados.

## Usuarios objetivo

### Operador
Usuario operativo que necesita ejecutar corridas con una interfaz clara, validaciones visibles y un flujo similar a software corporativo clásico.

Además, puede ajustar restricciones operativas visibles del sistema según la regla funcional acordada para la versión actual.

### Ingeniero
Usuario técnico-funcional que, además de ejecutar corridas, necesita ajustar configuración completa del sistema, parámetros del algoritmo y gestionar usuarios sin editar código fuente.

## Principios del producto

1. El producto principal es una aplicación de escritorio Windows.
2. La experiencia debe parecer software corporativo clásico, no una app web disfrazada.
3. Las validaciones deben ocurrir antes de ejecutar cuando sea posible.
4. Toda corrida debe dejar trazabilidad suficiente.
5. Los parámetros configurables no deben depender de editar código.
6. La documentación debe permitir que otro ingeniero continúe el desarrollo sin depender de conversaciones previas.
7. El crecimiento del sistema debe ordenarse por versiones y no por acumulación caótica de funcionalidades.

## Estado actual del roadmap

Las versiones V1.0, V1.1, V1.2 y V1.3 se consideran cerradas funcional y operativamente para el alcance definido hasta ahora.

Además, ya se validó un primer empaquetado técnico ejecutable del sistema como parte de la preparación de despliegue, aunque el instalador formal y la distribución siguen perteneciendo a una fase posterior.

## Roadmap por versiones

### V1.0 — Base operativa ✅ Cerrada
Objetivo:
- app desktop,
- entrada por Excel,
- modo `inicial`,
- validación de Excel,
- ejecución PSO,
- historial,
- detalle,
- exportación Excel,
- base de datos local de corridas.

### V1.1 — Interfaz operativa Windows ✅ Cerrada
Objetivo:
- menú superior,
- barra lateral de navegación,
- diálogos y navegación más cercanos a software Windows clásico,
- tablas y formularios más empresariales,
- mejor organización visual.

No cambia el núcleo del motor.

### V1.2 — Autenticación y perfiles ✅ Cerrada
Objetivo:
- autenticación real local,
- perfil Operador,
- perfil Ingeniero,
- restricciones de edición según perfil,
- base de datos de usuarios,
- cierre de sesión,
- gestión básica de usuarios por perfil Ingeniero.

### V1.3 — Configuración global editable ✅ Cerrada
Objetivo:
- pantalla de configuración del sistema,
- parámetros PSO editables por Ingeniero,
- restricciones operativas visibles y editables según regla acordada,
- persistencia global de configuración,
- restaurar valores por defecto,
- snapshot de configuración por corrida,
- visualización de resultados en interfaz mediante tabla y gráficos.

### V1.4 — Carga manual y gestión de corridas
Objetivo:
- captura manual de datos de entrada,
- edición manual de parámetros según perfil,
- validación fuerte de consistencia,
- construcción del mismo contrato interno que el flujo Excel,
- favoritos o casos base operativos,
- soporte de corridas base para futuras reprogramaciones,
- borrado automático mensual.

### V1.5 — Validación del modelo y reprogramación
Objetivo:
- definición de tolerancias,
- benchmark contra legacy,
- validación del modelo con ingeniero,
- definición e implementación de reprogramación.

### V1.6 — Integraciones, despliegue y cierre
Objetivo:
- scraping COES,
- alertas basadas en scraping y reglas operativas,
- decisión final sobre servidor propio,
- instalador Windows,
- distribución manual,
- actualización manual,
- transferencia y capacitación.