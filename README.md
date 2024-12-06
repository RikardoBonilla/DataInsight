# DataInsight

**DataInsight** es una aplicación de análisis de datos empresariales diseñada para ayudar a pequeñas y medianas empresas a tomar decisiones informadas basadas en sus datos operativos y de ventas.

## Características

- Importación de datos desde archivos CSV y Excel.
- Análisis de datos con cálculo de KPIs.
- Visualización interactiva de datos.
- Generación de reportes en PDF y Excel.
- Interfaz de usuario intuitiva y fácil de usar.

## Requisitos Previos

- Python 3.10 o superior
- Entorno virtual (recomendado)

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/RikardoBonilla/DataInsight.git

## Ejecución de Pruebas

Para ejecutar las pruebas unitarias:

```bash
python3 -m pytest

## Módulo de Análisis de Datos

El módulo `analytics.py` ubicado en `src/models/` proporciona funciones para:
- Calcular KPIs (ventas totales, margen de beneficio, etc.)
- Analizar tendencias (crecimiento mensual)
- Segmentar datos (por producto, región, etc.)

### Ejecución de Pruebas

Ejecutar todas las pruebas:

```bash
python3 -m pytest


## Módulo de Visualización y Reportes

El proyecto ahora incluye un módulo `plots.py` en `src/visualizations/` para generar gráficos a partir de los datos analizados.

- `plot_monthly_sales_trend`: Genera un gráfico de línea de las ventas mensuales.
- `plot_segmented_sales`: Genera un gráfico de barras agrupando por categorías.

También hay un módulo `report_generator.py` en `src/reports/` que permite crear reportes en PDF con KPIs y gráficos.

### Ejecución de las Pruebas

```bash
python3 -m pytest
