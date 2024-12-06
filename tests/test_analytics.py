# tests/test_analytics.py
import pytest
import pandas as pd
from src.models.analytics import total_sales, profit_margin, monthly_growth_rate, segment_data

def test_total_sales():
    data = {"ventas": [100, 200, 300]}
    df = pd.DataFrame(data)
    assert total_sales(df) == 600

def test_profit_margin():
    data = {"ingresos": [1000, 2000], "costos": [500, 800]}
    df = pd.DataFrame(data)
    pm = profit_margin(df)
    # Margen = (3000 - 1300) / 3000 = 1700/3000 ≈ 0.5666...
    assert pytest.approx(pm, 0.001) == 0.5667

def test_monthly_growth_rate():
    data = {
        "fecha": ["2021-01-15", "2021-01-20", "2021-02-10"],
        "ventas": [100, 200, 400]
    }
    df = pd.DataFrame(data)
    result = monthly_growth_rate(df)
    # Debe haber 2 meses: 2021-01 con 300, 2021-02 con 400
    # growth_rate de Febrero respecto a Enero = (400-300)/300 = 0.3333...
    growth = result.loc[result["year_month"] == "2021-02"]["growth_rate"].values[0]
    assert pytest.approx(growth, 0.001) == 0.3333

def test_segment_data():
    data = {
        "producto": ["A", "A", "B", "B"],
        "ventas": [100, 300, 200, 400]
    }
    df = pd.DataFrame(data)
    result = segment_data(df, "producto", "ventas")
    # Debe tener A:400 y B:600
    assert result.loc[result["producto"] == "A", "ventas"].values[0] == 400
    assert result.loc[result["producto"] == "B", "ventas"].values[0] == 600
