# tests/test_data_loader.py
import pytest
import pandas as pd
from src.services.data_loader import load_csv, load_excel, validate_data
import os

def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("archivo_inexistente.csv")

def test_load_excel_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_excel("archivo_inexistente.xlsx")

def test_validate_data():
    # Create a test DataFrame
    data = {
        "fecha": ["2021-01-01", "2021-01-02", None],
        "ventas": [100, 200, None]
    }

    df = pd.DataFrame(data)
    df_limpio = validate_data(df)

    # We expect it to remove the row with null values in date and sales.
    assert len(df_limpio) == 2
    assert "fecha" in df_limpio.columns
    assert df_limpio["fecha"].dtype == "datetime64[ns]"
