# Optimizacion Embalses

Aplicación de escritorio para ejecutar, consultar y exportar corridas de optimización de embalses, usando PySide6 como interfaz, SQLite como persistencia local y un motor PSO integrado en Python.

## Estado actual

### Producto principal
- Aplicación de escritorio en PySide6
- Ejecución local sin consumir HTTP
- Persistencia local en SQLite
- Flujo de entrada manual
- Flujo de entrada desde Excel
- Exportación de resultados a Excel
- Historial de corridas
- Detalle por corrida
- Integración operativa del motor PSO

### Soporte técnico disponible
- Backend FastAPI conservado como capa de soporte y diagnóstico
- Endpoint healthcheck
- Endpoints de corridas disponibles, pero ya no son el flujo principal de la aplicación

## Arquitectura actual

### Flujo principal
- `desktop_app/`: interfaz PySide6
- `backend/app/application/`: lógica de aplicación
- `backend/app/repositories/`: acceso a persistencia
- `backend/app/integrations/pso/`: motor PSO, lectura Excel y contratos
- `backend/corridas.db`: base SQLite local

### Flujo secundario
- `backend/app/api/`: API FastAPI conservada como soporte técnico, no como canal principal

## Estructura del proyecto

- `backend/`: lógica, persistencia, motor PSO, exportación Excel, soporte API
- `desktop_app/`: aplicación de escritorio PySide6
- `data_samples/`: archivos Excel de muestra para pruebas
- `docker-compose.yml`: infraestructura heredada de soporte para backend
- `.env.example`: variables de entorno de referencia

## Requisitos locales

### Entorno principal
- Python 3.11
- entorno virtual
- dependencias en `backend/requirements.txt`

## Base de datos local

La base activa en desarrollo local es:

```text
backend/corridas.db
```

## Ejecución local

1. Crear entorno e instalar dependencias

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Ejecutar aplicación de escritorio

Desde la raíz del proyecto:

```bash
backend\.venv\Scripts\python.exe desktop_app/app.py
```

## Flujos soportados
- manual
- excel mediante ruta local de archivo

## Validación funcional recomendada
- Crear corrida manual
- Crear corrida Excel
- Revisar historial
- Abrir detalle de corrida
- Exportar resultado a Excel
- Probar caso fallido con archivo inexistente
- Estado del motor PSO
- El motor PSO está integrado y operativo
- La aplicación ejecuta simulación, reparación, función objetivo, optimización y lectura desde Excel
- La salida operativa actual replica el flujo de Excel usado por el proceso legado
- La exportación principal vigente es Excel

## Limitaciones actuales
- No hay scraping implementado todavía
- No hay ingreso manual avanzado en pantalla todavía
- No hay autenticación
- No hay roles operador/ingeniero
- No hay migraciones de base de datos
- No hay procesamiento asíncrono de corridas largas
- FastAPI ya no es el flujo principal del producto
- Siguiente dirección del proyecto
- Limpieza técnica controlada del repositorio
- Mantener escritorio como producto principal
- Preparar integración futura para scraping
- Incorporar más adelante captura manual en pantalla
- Mantener la API solo como soporte mientras siga siendo útil