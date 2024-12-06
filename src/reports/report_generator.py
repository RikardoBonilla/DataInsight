# src/reports/report_generator.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import pandas as pd
from typing import Optional

def generate_pdf_report(output_file: str, kpis: dict, images: list):
    """
    Genera un reporte en PDF con KPIs y gráficas.
    
    :param output_file: Nombre del archivo PDF de salida.
    :param kpis: Diccionario con KPIs, ej {"Ventas Totales": 3000, "Margen": 0.2}
    :param images: Lista de rutas a imágenes (gráficos) a insertar en el reporte.
    :return: None
    """
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Título
    story.append(Paragraph("Reporte de Análisis de Datos - DataInsight", styles["Title"]))
    story.append(Spacer(1, 20))

    # KPIs
    story.append(Paragraph("KPIs:", styles["Heading2"]))
    for k, v in kpis.items():
        story.append(Paragraph(f"{k}: {v}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # Imágenes
    story.append(Paragraph("Visualizaciones:", styles["Heading2"]))
    for img_path in images:
        story.append(Image(img_path, width=400, height=200))
        story.append(Spacer(1, 20))
    
    doc.build(story)

def export_to_excel(df: pd.DataFrame, output_file: str = "analisis.xlsx"):
    """
    Exporta un DataFrame a un archivo Excel.
    
    :param df: DataFrame con datos a exportar.
    :param output_file: Nombre del archivo Excel de salida.
    :return: None
    """
    df.to_excel(output_file, index=False)
