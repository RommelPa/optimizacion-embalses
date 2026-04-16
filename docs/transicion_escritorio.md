# Transición a escritorio local

## Estado de la transición

La transición ya no está en evaluación.  
La decisión tomada es:

- interfaz principal: escritorio PySide6
- ejecución principal: local
- base de datos principal: SQLite local
- backend FastAPI: soporte secundario u opcional

---

## Motivo de la decisión

Se prioriza:
- operación local simple
- menor dependencia de red
- menor complejidad operativa
- mejor alineación con el uso esperado
- reutilización del núcleo de negocio ya implementado

---

## Principio arquitectónico

La aplicación de escritorio no debe depender del consumo HTTP para ejecutar el flujo principal.

La lógica de negocio debe vivir en:
- `backend/app/application`
- `backend/app/repositories`
- `backend/app/integrations/pso`

La aplicación de escritorio debe invocar esa lógica localmente.

---

## Flujo objetivo

1. UI PySide6 recopila datos.
2. Servicio local de escritorio llama a la capa de aplicación.
3. La capa de aplicación ejecuta la corrida.
4. Los resultados se guardan en SQLite.
5. La UI consulta historial, detalle y exporta Excel.

---

## Beneficios

- menor acoplamiento a FastAPI
- menor latencia local
- menos puntos de falla
- una sola fuente real de lógica de negocio
- escritorio más simple de desplegar internamente

---

## Implicancias

### Se conserva
- capa de aplicación
- repositorios
- integración PSO
- exportación Excel
- modelos y persistencia

### Se reduce a rol secundario
- API FastAPI
- endpoints HTTP como flujo principal

### Se elimina
- frontend web anterior
- cliente HTTP de escritorio para flujo normal

---

## Próximas decisiones esperadas

### Corto plazo
- limpiar residuos de frontend web
- limpiar residuos HTTP en escritorio
- limpiar documentación desactualizada
- consolidar configuración local

### Mediano plazo
- ingreso manual más rico en UI
- scraping como integración separada
- reglas operativas y validaciones avanzadas

### Largo plazo
- empaquetado de escritorio
- evaluación de servidor institucional solo si el scraping o sincronización lo exige