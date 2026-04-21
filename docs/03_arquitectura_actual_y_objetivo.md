# Arquitectura Actual y Dirección Objetivo

## Vista general

El proyecto está dividido en dos grandes zonas:

- `desktop_app`: interfaz de escritorio
- `backend/app`: lógica de negocio, persistencia, integración PSO y soporte API

## Flujo actual

1. La UI desktop recoge datos.
2. Un worker ejecuta la creación de corrida.
3. `CorridaLocalService` delega a `CorridaService`.
4. `CorridaService` arma el input del wrapper PSO.
5. El wrapper construye el contrato interno.
6. El lector Excel construye el `EngineInputContract`.
7. El engine PSO ejecuta optimización, reparación, simulación y cálculo de salida.
8. El resultado se guarda en SQLite.
9. La corrida puede verse en historial, detalle y exportarse.

## Capas principales

### Desktop
Responsable de:
- navegación,
- formularios,
- historial,
- detalle,
- exportación,
- ejecución en hilo separado.

### Application
Responsable de:
- caso de uso de corrida,
- persistencia de resultado,
- clasificación de estado,
- DTOs y errores.

### Integrations / PSO
Responsable de:
- wrapper,
- contratos,
- lector Excel,
- engine,
- función objetivo,
- simulación.

### Persistencia
Responsable de:
- base SQLite,
- modelo de corrida,
- repositorio.

## Arquitectura objetivo por etapas

### Estado actual
Base operativa establecida alrededor de `excel + inicial`.

### Próxima dirección
- rediseño visual tipo Windows clásico,
- autenticación,
- perfiles,
- configuración global editable,
- snapshot de configuración por corrida,
- carga manual,
- comparación entre corridas,
- reprogramación,
- scraping COES,
- alertas,
- posible evaluación de infraestructura central.

## Cambios arquitectónicos futuros relevantes

- La configuración del sistema dejará de vivir solo en constantes internas y pasará a persistencia editable.
- Se incorporará base de datos de usuarios.
- Se incorporará base de datos de configuración global.
- Cada corrida deberá guardar snapshot de configuración.
- La necesidad de servidor propio se evaluará antes de cualquier cambio de arquitectura de despliegue.
