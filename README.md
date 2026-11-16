# Explorador inteligente del recaudo tributario en Colombia

Proyecto de curso para explorar el recaudo por impuesto publicado por la DIAN y el recaudo anual registrado por dirección seccional. La primera fase normaliza las tablas; la regla mediana/MAD es la línea base de referencia para cambios mensuales inusuales. La comparación con otro método de detección queda para la siguiente fase.

## Datos

- `data/raw/`: archivos DIAN originales recibidos del equipo, preservados sin cambios.
- `data/processed/recaudo_anual_nacional.csv`: categorías nacionales, 1970 a septiembre de 2026.
- `data/processed/recaudo_mensual_nacional.csv`: todas las categorías numéricas de la tabla mensual DIAN, enero de 2000 a septiembre de 2026. Renta total e IVA interno conservan esos nombres para la línea base.
- `data/processed/recaudo_anual_seccional.csv`: categorías por dirección seccional, 2005 a septiembre de 2026.
- `docs/diccionario_datos.md`: procedencia, definiciones, unidades y límites.
- `docs/bitacora_ia.md`: registro inicial del uso de IA, pendiente de completar por el equipo.`r`n- `docs/Explorador_Recaudo_Tributario_hito2.pdf`: avance de una página para el hito 2.
- `results/baseline_alerts.csv` y `results/baseline_summary.json`: primera ejecución de la línea base.
- `results/ranking_seccionales_2025.csv`: comparación territorial para el último año completo.
- `results/annual_comparison_2024_2025.csv`: Renta e IVA para años completos recientes.

Los datos mensuales son nacionales; el desglose territorial es anual. La unidad territorial es la dirección seccional DIAN y no equivale necesariamente a la ciudad donde se originó el recaudo. Los valores están en millones de pesos corrientes. 2026 es parcial y preliminar; no se compara como año completo.

## Reproducir

Requiere Python 3.10 o superior. La preparación y la línea base usan solo la biblioteca estándar.

```powershell
python src/prepare_data.py
python src/baseline.py
```

La línea base usa solo Renta total e IVA interno; las demás categorías quedan disponibles para consultas y análisis posteriores. La regla compara cada mes con años anteriores del mismo mes calendario. Requiere seis años previos y marca una señal cuando la puntuación robusta absoluta es al menos 3,5. Las señales son exploratorias: no explican causas ni prueban evasión o irregularidad.

## Fuentes

DIAN, Estadísticas de Recaudo: https://www.dian.gov.co/dian/cifras/Paginas/EstadisticasRecaudo.aspx. Fecha de corte que reportan los archivos: 23 de octubre de 2026.

