# Visión del Producto y Versiones

## Propósito del sistema

Optimización de Embalses es una aplicación de escritorio para operadores e ingenieros del centro de control, diseñada para ejecutar corridas de optimización PSO de forma trazable, validada y operativamente usable, sin depender de manipulación directa del código.

El producto busca reemplazar el uso operativo del flujo legacy por una aplicación Windows clásica, con interfaz familiar para usuarios acostumbrados a herramientas tipo Microsoft Office, persistencia local y exportación controlada de resultados.

## Problema que resuelve

El proceso actual depende de lógica técnica especializada, flujo legacy y supuestos implícitos. Eso genera riesgos de:

- dependencia excesiva de personas que conocen el código,
- dificultad para replicar resultados,
- fragilidad en la validación de entradas,
- poca trazabilidad de qué configuración se usó en cada corrida,
- dificultad para evolucionar el algoritmo sin romper el flujo operativo.

## Usuarios objetivo

### Operador
Usuario operativo que necesita ejecutar corridas con una interfaz clara, validaciones visibles y un flujo similar a software corporativo clásico.

### Ingeniero / Programador
Usuario técnico-funcional que, además de ejecutar corridas, necesita ajustar configuración del sistema y parámetros del algoritmo sin entrar al código fuente.

### Otros actores
- TIC: soporte de instalación, distribución, pruebas en equipos y evaluación de infraestructura
- Contratista: responsable del entregable base de la Etapa 1 ya recibida

## Principios del producto

1. El producto principal es una aplicación de escritorio Windows.
2. La experiencia debe parecer software corporativo clásico, no una app web disfrazada.
3. Las validaciones deben ocurrir antes de ejecutar cuando sea posible.
4. Toda corrida debe dejar trazabilidad suficiente.
5. Los parámetros configurables no deben depender de editar código.
6. La documentación debe permitir que otro ingeniero continúe el desarrollo sin depender de conversaciones previas.
7. El crecimiento del sistema debe ordenarse por versiones y no por acumulación caótica de funcionalidades.

## Visión por versiones

### V1.0 — Base operativa
Incluye:
- app desktop,
- entrada por Excel,
- modo `inicial`,
- validación de Excel,
- ejecución PSO,
- historial,
- detalle,
- exportación Excel,
- base de datos local de corridas.

No incluye:
- interfaz corporativa final,
- autenticación,
- perfiles,
- configuración editable desde UI,
- carga manual,
- comparación entre corridas,
- reprogramación,
- scraping COES,
- alertas,
- servidor propio.

### V1.1 — Interfaz corporativa Windows
Incluye:
- menú superior,
- toolbar,
- diálogos y navegación más parecidos a software Windows clásico,
- tablas y formularios más empresariales,
- mejor organización visual.

No cambia todavía el núcleo del motor.

### V1.2 — Autenticación y perfiles
Incluye:
- autenticación real,
- perfil Operador,
- perfil Ingeniero / Programador,
- restricciones de edición según perfil,
- base de datos de usuarios.

### V1.3 — Configuración global editable
Incluye:
- pantalla de configuración del sistema,
- parámetros PSO editables por Ingeniero / Programador,
- restricciones operativas visibles y editables según regla acordada,
- persistencia global de configuración,
- restaurar valores por defecto,
- snapshot de configuración por corrida,
- evaluación de necesidad de servidor propio.

### V1.4 — Carga manual y gestión de corridas
Incluye:
- captura manual de datos de entrada,
- edición manual de parámetros según perfil,
- validación fuerte de consistencia,
- construcción del mismo contrato interno que el flujo Excel,
- comparación entre corridas,
- favoritos / casos base operativos,
- borrado automático mensual.

### V1.5 — Validación del modelo y reprogramación
Incluye:
- definición de tolerancias,
- benchmark contra legacy,
- validación del modelo con ingeniero,
- definición e implementación de reprogramación.

### V1.6 — Integraciones, despliegue y cierre
Incluye:
- scraping COES,
- alertas basadas en scraping y reglas operativas,
- decisión final sobre servidor propio,
- empaquetado,
- instalador Windows,
- distribución manual,
- actualización manual,
- transferencia y capacitación.

## Decisiones cerradas

- El stack oficial de interfaz es PySide6 / Qt.
- No se migrará a Java.
- La UI evolucionará hacia estilo Windows clásico.
- Habrá autenticación real.
- Habrá perfiles reales.
- Los parámetros configurables del sistema serán persistentes.
- Cada corrida deberá guardar snapshot de configuración.
- La distribución inicial será manual.
- La actualización inicial será manual.
- Se buscará instalador real para Windows.
- La necesidad de servidor propio se evaluará, no se asume desde el inicio.
