# Optimización de Embalses

Aplicación de escritorio para ejecutar, consultar y exportar corridas de optimización de embalses, usando **PySide6** como interfaz, **SQLite** como persistencia local y un motor **PSO** modularizado en Python.

## Estructura del proyecto

* `backend/`: lógica, persistencia, integración PSO, exportación Excel y soporte API.
* `desktop_app/`: aplicación de escritorio.
* `data_samples/`: archivos de ejemplo para pruebas.
* `docs/`: documentación funcional y técnica del proyecto.

## Requisitos locales

* Python 3.11
* Windows
* entorno virtual

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
