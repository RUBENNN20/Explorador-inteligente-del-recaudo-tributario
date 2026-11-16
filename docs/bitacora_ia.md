# Bitácora humano-IA

Registro inicial. Los integrantes deben añadir sus nombres, verificar los resultados y actualizar qué decisiones aceptaron, modificaron o descartaron antes de entregar.

| Fecha | Integrante | Herramienta | Uso | Qué se aceptó, modificó o descartó | Cómo se verificó |
|---|---|---|---|---|---|
| 2026-11-11 | Completar por el equipo | ChatGPT (Codex) | Revisar cobertura, categorías y granularidad de los archivos DIAN. | Propuesta provisional: separar la serie mensual nacional del desglose anual por seccional. Se descartó modelar alertas mensuales por ciudad porque esa combinación de datos no está disponible en los archivos recibidos. El equipo debe confirmar esta decisión. | Inspección de encabezados, periodos, valores y notas de los tres archivos; revisar el resultado con cada integrante. |
| 2026-11-11 | Completar por el equipo | ChatGPT (Codex) | Preparar las tablas normalizadas y ejecutar una primera regla de referencia para señalar cambios mensuales inusuales en Renta e IVA. | Se propone mediana/MAD del mismo mes calendario como línea base; el umbral queda sujeto a discusión y justificación del equipo. Se excluye 2026 del puntaje comparativo porque está incompleto. | Reejecución de `src/prepare_data.py` y `src/baseline.py`; revisar `results/baseline_summary.json` y las alertas frente al archivo original. |
| 2026-11-14 | Completar por el equipo | ChatGPT (Codex) | Revisar por qué la primera tabla mensual solo contenía Renta total e IVA interno y ampliar la preparación. | Se amplió el CSV mensual para conservar todas las columnas numéricas de tributos; la línea base sigue limitada provisionalmente a esas dos series para mantener comparable el primer resultado. | Se volvió a generar el CSV desde el Excel fuente, se compararon sus categorías con los encabezados DIAN y se reejecutó la línea base. |

## Reflexión inicial sobre el uso de IA

En la conversación, la IA inicialmente sugirió detectar cambios mensuales por seccional. Al revisar los archivos, se comprobó que el desglose por seccional disponible es anual y que la serie mensual es nacional. Por eso, la propuesta de alcance se ajustó. Esta revisión muestra que una respuesta de IA puede describir una granularidad que los datos realmente no tienen; el equipo debe comprobar cada afirmación contra las fuentes antes de presentar conclusiones.
