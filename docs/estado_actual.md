# Estado actual del proyecto

## Decisión vigente

La aplicación principal del proyecto es ahora una aplicación de escritorio en PySide6.

El backend mantiene:
- la lógica de aplicación
- el acceso a base de datos
- la integración con el motor PSO
- la exportación a Excel

La API FastAPI queda como interfaz secundaria y opcional, no como flujo principal del producto.

---

## Flujo principal actual

1. El usuario crea una corrida desde la aplicación de escritorio.
2. La aplicación de escritorio invoca localmente la capa de aplicación.
3. La capa de aplicación ejecuta el wrapper PSO.
4. Se persiste la corrida en SQLite.
5. El usuario consulta historial, detalle y exportación Excel desde escritorio.

---

## Funcionalidad validada

### Corridas
- creación de corrida manual
- creación de corrida desde Excel local
- persistencia de corridas
- manejo de errores de validación
- manejo de errores de ejecución

### Consulta
- historial de corridas
- detalle de corrida
- visualización de datos clave
- exportación Excel legacy

### Motor
- lectura desde Excel
- construcción del contrato del motor
- ejecución PSO
- almacenamiento de resultados
- generación de gráficos para exportación Excel

---

## Base de datos

Base actual:
- SQLite local

Ubicación actual:
- `backend/corridas.db`

---

## Interfaz principal actual

Aplicación de escritorio:
- PySide6

Módulos activos:
- nueva corrida
- historial
- detalle
- exportación Excel

---

## Arquitectura vigente

### Backend
- `app/application`: casos de uso y orquestación
- `app/repositories`: acceso a persistencia
- `app/integrations/pso`: motor y lectura de entradas
- `app/models`: modelos ORM
- `app/db`: sesión y configuración de base de datos
- `app/api`: interfaz HTTP opcional

### Escritorio
- `desktop_app/ui`: pantallas PySide6
- `desktop_app/services`: integración local con capa de aplicación

---

## Alcance actual

Soportado:
- origen manual
- origen Excel local
- exportación Excel

No implementado aún:
- ingreso manual detallado en pantalla
- scraping web
- alertas automáticas
- autenticación
- roles
- procesamiento asíncrono
- despliegue institucional

---

## Próximas líneas de trabajo

1. limpieza técnica del repositorio
2. consolidación de la arquitectura escritorio + backend local
3. preparación del ingreso manual en pantalla
4. diseño del módulo futuro de scraping
5. endurecimiento de validaciones y empaquetado