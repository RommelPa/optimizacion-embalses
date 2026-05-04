# Arquitectura técnica

## Diagrama general de arquitectura

![Diagrama general de arquitectura](./img/arquitectura.png)

### Aclaraciones

- `desktop_app` concentra la experiencia de usuario: login, navegación, formularios, historial, detalle, configuración y gestión de usuarios.
- `backend/app` concentra la lógica del sistema: casos de uso, servicios, validaciones, acceso a datos, configuración global y coordinación con el motor.
- `SQLite` almacena la información persistente del sistema, incluyendo corridas, usuarios y configuración.
- El `motor PSO` ejecuta la lógica de optimización y devuelve resultados que luego son persistidos y mostrados en la interfaz.
- La aplicación ya fue validada tanto en ejecución de desarrollo como en un primer empaquetado técnico ejecutable.

## Flujo de corrida

![Diagrama de flujo de corrida](./img/flujo.png)

### Aclaraciones

- `Login` valida credenciales antes de abrir la aplicación principal.
- `MainWindow` actúa como contenedor de navegación de la aplicación.
- `Nueva corrida` recoge los datos del caso y dispara la ejecución.
- `Worker` ejecuta la corrida en un hilo separado para no bloquear la UI.
- `CorridaService` coordina el caso de uso de creación de corrida.
- `Wrapper PSO` adapta la entrada del sistema al contrato requerido por el motor.
- `Engine` ejecuta la optimización y genera resultados.
- `SQLite` persiste la corrida, la configuración usada y la trazabilidad operativa.
- `Historial`, `Detalle` y `Exportación` consumen la información persistida para consulta operativa.
- `Configuración` y `Usuarios` aplican permisos por rol según las reglas funcionales vigentes.

## Estado actual de la arquitectura

A la fecha, la arquitectura validada incluye:

- aplicación desktop funcional,
- autenticación local con perfiles,
- gestión de usuarios,
- configuración global persistente,
- snapshot de configuración por corrida,
- visualización de resultados en tabla y gráficos,
- exportación Excel,
- persistencia local en SQLite,
- ejecución validada fuera del IDE,
- primer empaquetado técnico ejecutable validado.

## Extensiones futuras

Las siguientes capacidades están previstas en el roadmap, pero no forman parte del flujo base actual:

- carga manual,
- favoritos o casos base,
- reprogramación como servicio separado sobre el mismo contrato de entrada,
- scraping COES,
- alertas internas del sistema,
- alertas externas mediante mecanismos gratuitos,
- instalador formal y despliegue final.