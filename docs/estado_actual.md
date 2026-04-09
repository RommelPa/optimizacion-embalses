# Estado actual del proyecto

## Resumen
El proyecto ya cuenta con frontend y backend funcionales, integración del motor PSO, persistencia de corridas, historial, detalle y filtros básicos.

## Funcionalidades operativas actuales
- Crear corrida manual
- Crear corrida con Excel local
- Ejecutar motor PSO
- Persistir corridas exitosas y fallidas
- Consultar historial
- Consultar detalle por corrida
- Filtrar historial por:
  - origen_datos
  - estado
  - id
  - fecha_proceso

## Backend
- FastAPI
- SQLite local por defecto
- PostgreSQL funcionando con Docker Compose
- Endpoints principales disponibles en `/api/v1`

## Frontend
- Next.js
- navegación básica entre:
  - inicio
  - corridas
  - historial
  - detalle

## Integración PSO
- wrapper separado
- mapper de entrada
- lector Excel
- contrato de entrada formal
- motor modularizado por capas

## Limitaciones actuales
- no hay upload real de archivos
- no hay autenticación
- no hay migraciones
- frontend no dockerizado
- no hay ejecución asíncrona