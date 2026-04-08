# Optimizacion Embalses

Aplicación web para ejecutar y consultar corridas de optimización de embalses, con backend en FastAPI, frontend en Next.js e integración progresiva de motor PSO.

## Estado actual

### Ya implementado
- Frontend web con navegación básica
- Backend FastAPI
- Endpoint healthcheck
- Creación de corridas
- Integración del motor PSO
- Flujo manual y flujo Excel
- Validaciones y manejo de errores
- Persistencia básica de corridas
- Historial de corridas
- Detalle por corrida
- Filtros en historial
- Resumen simple en historial

### Flujos soportados
- `manual`
- `excel` mediante ruta local de archivo

### Persistencia actual
- SQLite local por defecto
- Preparación parcial para PostgreSQL + Docker

## Estructura del proyecto

- `backend/`: API FastAPI, persistencia, integración PSO
- `frontend/`: aplicación Next.js
- `data_samples/`: archivos de muestra locales
- `docker-compose.yml`: base para backend + postgres
- `.env.example`: variables de entorno de ejemplo

## Requisitos locales

### Backend
- Python 3.11
- entorno virtual
- dependencias en `backend/requirements.txt`

### Frontend
- Node.js
- npm

## Ejecución local sin Docker

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```