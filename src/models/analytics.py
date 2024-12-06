# src/models/analytics.py
import pandas as pd
import numpy as np
from typing import Optional

def total_sales(df: pd.DataFrame, sales_column: str = "ventas") -> float:
    """
    Calcula las ventas totales de un DataFrame.
    
    :param df: DataFrame con datos de ventas.
    :param sales_column: Nombre de la columna que contiene las ventas.
    :return: Suma total de las ventas.
    :raises ValueError: Si la columna de ventas no existe o es vacía.
    """
    if sales_column not in df.columns:
        raise ValueError(f"La columna {sales_column} no existe en el DataFrame.")
    return df[sales_column].sum()

def profit_margin(df: pd.DataFrame, revenue_col: str = "ingresos", cost_col: str = "costos") -> float:
    """
    Calcula el margen de beneficio como (ingresos - costos) / ingresos.
    
    :param df: DataFrame con datos de ingresos y costos.
    :param revenue_col: Nombre de la columna con ingresos.
    :param cost_col: Nombre de la columna con costos.
    :return: Margen de beneficio en formato decimal. Ej: 0.2 significa 20%.
    :raises ValueError: Si no existen las columnas o si ingresos es cero.
    """
    if revenue_col not in df.columns or cost_col not in df.columns:
        raise ValueError("Las columnas de ingresos y/o costos no existen en el DataFrame.")

    total_revenue = df[revenue_col].sum()
    total_cost = df[cost_col].sum()

    if total_revenue == 0:
        raise ValueError("Los ingresos totales son cero, no se puede calcular el margen de beneficio.")

    return (total_revenue - total_cost) / total_revenue

def monthly_growth_rate(df: pd.DataFrame, date_col: str = "fecha", sales_col: str = "ventas") -> pd.DataFrame:
    """
    Calcula el crecimiento mensual de las ventas.
    
    :param df: DataFrame con columna de fecha y ventas.
    :param date_col: Nombre de la columna con las fechas.
    :param sales_col: Nombre de la columna con las ventas.
    :return: DataFrame con columnas [mes, ventas_mensuales, growth_rate].
    """
    if date_col not in df.columns or sales_col not in df.columns:
        raise ValueError(f"Columnas {date_col} y/o {sales_col} no disponibles.")
    
    # Asegurar que la fecha está en datetime
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    # Agrupar por mes y año
    df["year_month"] = df[date_col].dt.to_period("M")
    monthly_data = df.groupby("year_month")[sales_col].sum().reset_index()
    monthly_data["year_month"] = monthly_data["year_month"].astype(str)

    # Calcular tasa de crecimiento: (ventas_mes_actual - ventas_mes_anterior) / ventas_mes_anterior
    monthly_data["growth_rate"] = monthly_data[sales_col].pct_change()

    return monthly_data

def segment_data(df: pd.DataFrame, segment_col: str, agg_col: str = "ventas") -> pd.DataFrame:
    """
    Segmenta el DataFrame por la columna segment_col y calcula la suma del agg_col para cada segmento.
    
    :param df: DataFrame con los datos.
    :param segment_col: Columna por la cual segmentar (ej. 'producto', 'region').
    :param agg_col: Columna que se va a agregar (por defecto 'ventas').
    :return: DataFrame con columnas [segment_col, agg_col] agregadas por segmento.
    :raises ValueError: Si las columnas no existen en el DataFrame.
    """
    if segment_col not in df.columns:
        raise ValueError(f"La columna {segment_col} no existe en el DataFrame.")
    if agg_col not in df.columns:
        raise ValueError(f"La columna {agg_col} no existe en el DataFrame.")

    result = df.groupby(segment_col)[agg_col].sum().reset_index()
    return result
