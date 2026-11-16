# Diccionario de datos y procedencia

## Fuentes

Los tres archivos originales están preservados sin cambios en `data/raw/` y fueron entregados por el equipo. Procedencia institucional: Dirección de Impuestos y Aduanas Nacionales (DIAN), Estadísticas de Recaudo, https://www.dian.gov.co/dian/cifras/Paginas/EstadisticasRecaudo.aspx. Fecha de corte indicada por los archivos: 23 de octubre de 2026.

## Archivos preparados

| Archivo | Qué representa | Cobertura | Unidad |
|---|---|---:|---|
| `recaudo_anual_nacional.csv` | Valores por categoría tributaria publicados por la DIAN, en formato largo. Conserva subtotales y componentes por separado. | 1970 a septiembre de 2026 | Millones de pesos corrientes |
| `recaudo_mensual_nacional.csv` | Renta total e IVA interno por mes para Colombia. | Enero de 2000 a septiembre de 2026 | Millones de pesos corrientes |
| `recaudo_anual_seccional.csv` | Valores anuales por dirección seccional y categoría de tributo. | 2005 a septiembre de 2026 | Millones de pesos corrientes |

`2026` es preliminar y parcial a septiembre, por lo que no se compara como año completo en la línea base mensual ni en el ranking territorial. La publicación territorial informa que, para septiembre de 2026, está pendiente de reportar 3,97% del recaudo bruto observado.

## Definiciones y límites

- La línea base inicial selecciona `Renta total` y `IVA interno`; el CSV también conserva las demás categorías mensuales, subtotales y componentes publicados.
- `Renta total` de la serie mensual corresponde a renta cuotas más retención a título de renta.
- `IVA interno` corresponde a declaraciones de IVA más retención a título de IVA. La tabla anual también registra por separado el IVA externo asociado a la actividad externa. `IVA total (interno + externo)` en el archivo comparativo es una suma derivada de esas dos categorías distintas.
- Las tablas contienen recaudo bruto en millones de pesos corrientes; las variaciones entre años no están ajustadas por inflación.
- Una dirección seccional es la unidad territorial/administrativa de publicación de la DIAN. No permite afirmar que todo el recaudo se originó en la ciudad de su nombre.
- Los totales y componentes se conservan por separado. No sumar subtotales junto con sus componentes, pues se duplicaría el recaudo.
- Las señales estadísticas identifican valores que se apartan del patrón histórico; no explican causas ni son evidencia de evasión o irregularidad.

