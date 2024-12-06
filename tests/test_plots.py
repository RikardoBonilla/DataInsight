# tests/test_plots.py
import pytest
import pandas as pd
from src.visualizations.plots import plot_monthly_sales_trend, plot_segmented_sales
import os

def test_plot_monthly_sales_trend(tmp_path):
    data = {
        "fecha": ["2021-01-10", "2021-01-20", "2021-02-15"],
        "ventas": [100, 200, 300]
    }
    df = pd.DataFrame(data)
    output_file = str(tmp_path / "monthly_sales.png")
    plot_monthly_sales_trend(df, "fecha", "ventas", output_file)
    assert os.path.exists(output_file)

def test_plot_segmented_sales(tmp_path):
    data = {
        "producto": ["A", "A", "B"],
        "ventas": [100, 200, 300]
    }
    df = pd.DataFrame(data)
    output_file = str(tmp_path / "segmented_sales.png")
    plot_segmented_sales(df, "producto", "ventas", output_file)
    assert os.path.exists(output_file)
