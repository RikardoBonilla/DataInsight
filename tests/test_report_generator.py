# tests/test_report_generator.py
import pytest
from src.reports.report_generator import generate_pdf_report
import os

def test_generate_pdf_report(tmp_path):
    kpis = {"Ventas Totales": 1000, "Margen": 0.25}
    output_file = str(tmp_path / "reporte.pdf")
    images = []  # Puedes no tener imágenes en la prueba inicial
    generate_pdf_report(output_file, kpis, images)
    assert os.path.exists(output_file)
