# src/visualizations/plots.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

def plot_monthly_sales_trend(df: pd.DataFrame, date_col: str = "fecha", sales_col: str = "ventas", output_file: str = "monthly_sales.png"):
    """
    Genera un gráfico de línea mostrando la tendencia mensual de ventas.
    
    :param df: DataFrame con los datos.
    :param date_col: Columna con las fechas.
    :param sales_col: Columna con las ventas.
    :param output_file: Nombre del archivo de salida para el gráfico.
    :return: None
    """
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df["year_month"] = df[date_col].dt.to_period("M")
    monthly_data = df.groupby("year_month")[sales_col].sum().reset_index()
    monthly_data["year_month"] = monthly_data["year_month"].astype(str)

    plt.figure(figsize=(10,6))
    sns.lineplot(data=monthly_data, x="year_month", y=sales_col, marker="o")
    plt.xticks(rotation=45)
    plt.title("Tendencia Mensual de Ventas")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def plot_segmented_sales(df: pd.DataFrame, segment_col: str, sales_col: str = "ventas", output_file: str = "segmented_sales.png"):
    """
    Genera un gráfico de barras con las ventas agrupadas por un segmento específico.
    
    :param df: DataFrame con los datos.
    :param segment_col: Columna por la cual segmentar (ej. 'producto').
    :param sales_col: Columna con las ventas.
    :param output_file: Nombre del archivo de salida.
    :return: None
    """
    if segment_col not in df.columns or sales_col not in df.columns:
        raise ValueError("Columnas faltantes para generar el gráfico segmentado.")
    
    segment_data = df.groupby(segment_col)[sales_col].sum().reset_index()

    plt.figure(figsize=(10,6))
    sns.barplot(data=segment_data, x=segment_col, y=sales_col)
    plt.title(f"Ventas por {segment_col}")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
