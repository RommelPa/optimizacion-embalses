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
- Persistencia de corridas
- Historial de corridas
- Detalle por corrida
- Filtros en historial
- Resumen simple en historial
- Soporte local con SQLite
- Soporte backend + PostgreSQL con Docker Compose

### Flujos soportados
- `manual`
- `excel` mediante ruta local de archivo

### Persistencia actual
- SQLite local por defecto
- PostgreSQL al ejecutar backend con Docker Compose

## Estructura del proyecto

- `backend/`: API FastAPI, persistencia, integración PSO
- `frontend/`: aplicación Next.js
- `data_samples/`: archivos locales de muestra para pruebas
- `docker-compose.yml`: backend + PostgreSQL
- `.env.example`: variables de entorno de ejemplo

## Requisitos locales

### Backend
- Python 3.11
- entorno virtual
- dependencias en `backend/requirements.txt`

### Frontend
- Node.js
- npm

### Docker
- Docker Desktop
- virtualización habilitada

## Variables de entorno

### Frontend
Archivo:

```text
frontend/.env.local
```

Contenido mínimo
```text
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Docker/PostgreSQL
Archivo en la raíz del proyecto
```text
.env
```

Contenido base
```text
POSTGRES_DB=optimizacion_embalses
POSTGRES_USER=optimizacion_user
POSTGRES_PASSWORD=optimizacion_pass
DATABASE_URL=postgresql+psycopg://optimizacion_user:optimizacion_pass@db:5432/optimizacion_embalses
NEXT_PUBLIC_API_URL=http://localhost:8000
```
### Ejecución local sin Docker
Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend
```bash
cd frontend
npm install
npm run dev
```

Base usada en modo local
- SQLite local por defecto
- Archivo: 
```text
backend/corridas.db
```

### Ejecución con Docker (backend + PostgreSQL)
- Docker Desktop corriendo
- Archivo .env en la raíz del proyecto

```bash
docker compose up --build
```

Servicios levantados
```text
PostgreSQL en localhost:5432
Backend en localhost:8000
```

Nota importante
- En esta etapa, el frontend sigue ejecutándose localmente fuera de Docker.

Validación mínima después de levantar
Backend
Probar:
```text
GET /api/v1/health
GET /api/v1/corridas
POST /api/v1/corridas
```
Swagger:
```text
http://localhost:8000/docs
```

Frontend
Abrir:
```text
http://localhost:3000/
http://localhost:3000/corridas
http://localhost:3000/historial
```

Flujo recomendado de validación
1. Crear corrida manual
2. Crear corrida excel
3. Revisar historial
4. Abrir detalle de corrida
5. Probar caso fallido con archivo inexistente

Endpoints principales backend
```text
GET /api/v1/health
POST /api/v1/corridas
GET /api/v1/corridas
GET /api/v1/corridas/{id}
```

Rutas principales frontend
```text
/
/corridas
/historial
/historial/[id]
```
Estado actual del motor PSO
- El núcleo del motor PSO está integrado y operativo dentro del backend.
- La aplicación ya ejecuta simulación, reparación, función objetivo, optimización y lectura base desde Excel.
- El motor puede ejecutarse desde la API y sus resultados se muestran en frontend.
- La generación de gráficos y la exportación Excel del script original aún no han sido integradas al flujo web.
- Actualmente el sistema usa el PSO como motor de cálculo y ejecución, no como réplica completa 1:1 de toda la salida del script legacy.

Limitaciones actuales
- No hay upload real de archivos todavía
- El flujo Excel usa ruta local temporal
- El frontend no está dockerizado
- No hay autenticación
- No hay roles operador/ingeniero
- No hay migraciones de base de datos
- No hay procesamiento asíncrono de corridas largas
- Trabajo recomendado siguiente
- Cerrar handoff/documentación técnica de esta fase
- Evaluar migraciones de base de datos
- Definir si el siguiente paso será Docker completo o funcionalidad de producto
- Preparar despliegue on-prem

Trabajo recomendado siguiente
- Cerrar handoff y documentación técnica de esta fase
- Evaluar migraciones de base de datos
- Definir si el siguiente bloque será infraestructura o funcionalidad operativa
- Preparar despliegue on-prem
- Definir si la salida legacy (gráficos y Excel) se replicará como exportación o se migrará progresivamente a visualización web