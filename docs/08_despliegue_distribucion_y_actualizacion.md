# Despliegue, Distribución y Actualización

## Objetivo

Definir cómo se empaquetará, distribuirá, instalará y actualizará la aplicación en el alcance actual del proyecto.

## Decisiones actuales

- Se buscará un instalador real para Windows.
- La distribución inicial será manual.
- La actualización inicial será manual.
- TIC participará en pruebas de instalación y validación en equipos.
- La necesidad de servidor propio queda como evaluación, no como implementación cerrada.

## Empaquetado

El sistema deberá:
- generar un paquete instalable para Windows,
- incluir las dependencias necesarias,
- permitir ejecución estable en equipos objetivo,
- validar creación de la base local y carpetas necesarias.

## Distribución

La distribución inicial será manual. Eso implica:
- definir quién entrega la versión,
- definir dónde se publica o comparte el instalador,
- definir la nomenclatura de versiones,
- definir cómo se comunica una nueva entrega.

## Instalación

Debe probarse:
- instalación en laptop limpia,
- arranque correcto,
- lectura de configuración,
- creación y uso de base de datos local,
- exportación de resultados.

## Actualización

La actualización inicial será manual. Eso implica:
- definir procedimiento de reemplazo o instalación de nueva versión,
- validar que no se pierdan corridas locales,
- validar que no se pierda configuración local,
- documentar el procedimiento para usuarios y soporte.

## Evaluación de servidor propio

El servidor propio no se asume como requisito inmediato. Primero debe evaluarse:

- qué problema resolvería,
- si se necesita para configuración central, alertas o distribución,
- qué implicancias tendría para TIC,
- qué impacto tendría en seguridad, soporte y mantenimiento.

## Pendientes documentales

- herramienta final de empaquetado,
- formato final del instalador,
- canal exacto de distribución interna,
- procedimiento documentado de actualización manual.
