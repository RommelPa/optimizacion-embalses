# Optimización de Embalses

Aplicación de escritorio para ejecutar, consultar y exportar corridas de optimización de embalses, usando **PySide6** como interfaz, **SQLite** como persistencia local y un motor **PSO** modularizado en Python.

## Estado del producto

### Base operativa actual

La base operativa actual permite:

- ejecutar corridas desde archivo Excel,
- trabajar en modo de operación `inicial`,
- validar la entrada antes de correr,
- consultar historial de corridas,
- revisar detalle de resultados,
- exportar resultados a Excel,
- guardar corridas y resultados en base de datos local SQLite.

### Alcance global por versiones

El proyecto está organizado por versiones evolutivas:

- **V1.0**: base operativa
- **V1.1**: interfaz corporativa Windows clásica
- **V1.2**: acceso y perfiles
- **V1.3**: configuración global editable
- **V1.4**: carga manual y gestión de corridas
- **V1.5**: validación del modelo y reprogramación
- **V1.6**: integraciones, despliegue y cierre

## Arquitectura actual

### Flujo principal

- `desktop_app/`: interfaz de escritorio en PySide6
- `backend/app/application/`: lógica de aplicación
- `backend/app/repositories/`: acceso a persistencia
- `backend/app/models/`: modelo de datos
- `backend/app/db/`: inicialización y sesión de base de datos
- `backend/app/integrations/pso/`: integración del motor PSO, contratos, lectura Excel y engine

### Flujo secundario

- `backend/app/api/`: API FastAPI conservada como soporte técnico heredado, no como flujo principal del producto

## Estructura del proyecto

- `backend/`: lógica, persistencia, integración PSO, exportación Excel y soporte API
- `desktop_app/`: aplicación de escritorio
- `data_samples/`: archivos de ejemplo para pruebas
- `docs/`: documentación funcional y técnica del proyecto

## Requisitos locales

- Python 3.11
- Windows
- entorno virtual

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/RommelPa/optimizacion-embalses.git
cd optimizacion-embalses
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

En Windows CMD:

```bash
.venv\Scripts\activate
```

En PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución de la aplicación desktop

Desde la raíz del proyecto:

```bash
python desktop_app/app.py
```

## Base de datos local

La aplicación crea y usa una base SQLite local en:

```text
backend/corridas.db
```

## Flujo funcional actual

1. Abrir la aplicación desktop.
2. Ir a **Nueva corrida**.
3. Ingresar:
   - caso de estudio,
   - fecha de proceso,
   - observaciones opcionales.
4. Seleccionar el archivo Excel de entrada.
5. Ejecutar la corrida.
6. Revisar el resultado.
7. Consultar historial.
8. Abrir detalle.
9. Exportar el resultado a Excel.

## Plantilla Excel oficial

La corrida base debe ejecutarse usando la plantilla oficial:

- `Plantilla_Entrada_V1.xlsx`

## Despliegue previsto

- instalación local en Windows,
- instalador real para Windows,
- distribución inicial manual,
- actualización inicial manual,
- evaluación de necesidad de servidor propio en versiones posteriores.

## Documentación disponible

- `docs/00_vision.md`
- `docs/01_contrato_funcional_global.md`
- `docs/02_contrato_excel_entrada_v1.md`
- `docs/03_arquitectura_actual_y_objetivo.md`
- `docs/04_plan_implementacion_y_versiones.md`
- `docs/05_plantilla_excel_oficial.md`
- `docs/06_guia_pso.md`
- `docs/07_perfiles_y_configuracion.md`
- `docs/08_despliegue_distribucion_y_actualizacion.md`

## Qué cubre la documentación

### `00_vision.md`
Explica la visión del producto, los usuarios objetivo, principios del sistema y el alcance por versiones.

### `01_contrato_funcional_global.md`
Describe el comportamiento funcional actual y la evolución prevista del sistema.

### `02_contrato_excel_entrada_v1.md`
Define la estructura oficial del Excel de entrada y sus reglas de validación.

### `03_arquitectura_actual_y_objetivo.md`
Resume la arquitectura actual, las capas del sistema y la dirección técnica futura.

### `04_plan_implementacion_y_versiones.md`
Ordena el desarrollo por versiones y define la secuencia de implementación.

### `05_plantilla_excel_oficial.md`
Describe la plantilla Excel oficial y su propósito operativo.

### `06_guia_pso.md`
Explica cómo está modularizado el PSO y qué archivo tocar según el tipo de cambio.

### `07_perfiles_y_configuracion.md`
Define perfiles, permisos y futura configuración editable del sistema.

### `08_despliegue_distribucion_y_actualizacion.md`
Describe empaquetado, distribución, actualización y evaluación de infraestructura futura.

## Limitaciones actuales

- no hay reprogramación activa,
- no hay carga manual activa,
- no hay autenticación todavía,
- no hay perfiles todavía,
- la configuración aún vive principalmente en constantes internas,
- las tolerancias numéricas contra benchmark legacy aún deben validarse con el ingeniero especialista,
- scraping COES y alertas aún no están implementados,
- la distribución y actualización automáticas aún no forman parte del alcance actual.

## Estado del motor PSO

El motor PSO está modularizado y separado por responsabilidades:

- contrato externo del wrapper,
- contrato interno del engine,
- lectura y validación del Excel,
- runner del engine,
- optimización PSO,
- función objetivo,
- reparación de solución,
- simulación hidráulica.

La guía técnica está en:

- `docs/06_guia_pso.md`
