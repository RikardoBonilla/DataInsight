# src/ui/app.py
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.services.data_loader import load_csv, load_excel, validate_data
from src.models.analytics import total_sales, profit_margin, monthly_growth_rate, segment_data
from src.visualizations.plots import plot_monthly_sales_trend, plot_segmented_sales
from src.reports.report_generator import generate_pdf_report

# Inicializar la app de Dash con un tema de Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("DataInsight Dashboard"),
    html.Hr(),
    dcc.Store(id='data-store', storage_type='memory'),

    # Componente de subida de archivo
    html.Div([
        html.Label("Cargar Datos (CSV o Excel):"),
        dcc.Upload(
            id='file-upload',
            children=html.Div(['Arrastra o haz click para seleccionar un archivo']),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center'
            }
        ),
        html.Div(id='upload-status')
    ], style={'margin-bottom': '30px'}),

    # Dropdown para segmentar datos
    html.Div([
        html.Label("Seleccionar Segmento:"),
        dcc.Dropdown(id='segment-dropdown', options=[], value=None)
    ], style={'margin-bottom': '30px'}),

    # Gráficos
    dcc.Graph(id='monthly-sales-graph'),
    dcc.Graph(id='segment-sales-graph'),

    # Botón para generar reporte
    html.Button("Generar Reporte PDF", id='generate-report-button'),
    html.Div(id='report-status'),
], fluid=True)

@app.callback(
    [Output('data-store', 'data'),
     Output('upload-status', 'children')],
    [Input('file-upload', 'contents')],
    [State('file-upload', 'filename')]
)
def process_uploaded_file(contents, filename):
    if contents is None:
        return None, "No hay archivo cargado."

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    df = None
    if filename.endswith('.csv'):
        df = load_csv(io.StringIO(decoded.decode('utf-8')))
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        df = load_excel(io.BytesIO(decoded))

    if df is not None:
        df = validate_data(df)
        return df.to_dict('records'), f"Archivo {filename} cargado y validado exitosamente."
    else:
        return None, "No se pudo cargar el archivo o el formato no es soportado."

@app.callback(
    Output('segment-dropdown', 'options'),
    Input('data-store', 'data')
)
def update_segment_options(data):
    if data is None:
        return []
    df = pd.DataFrame(data)
    if 'producto' in df.columns:
        productos = df['producto'].unique()
        return [{'label': p, 'value': p} for p in productos]
    return []

@app.callback(
    [Output('monthly-sales-graph', 'figure'),
     Output('segment-sales-graph', 'figure')],
    [Input('data-store', 'data'),
     Input('segment-dropdown', 'value')]
)
def update_graphs(data, segmento):
    if data is None:
        return {}, {}

    df = pd.DataFrame(data)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df.dropna(subset=['fecha'])

    # Calcular ventas mensuales
    monthly_data = df.groupby(df['fecha'].dt.to_period("M"))['ventas'].sum().reset_index()
    monthly_data['fecha'] = monthly_data['fecha'].astype(str)

    fig_monthly = {
        'data': [{'x': monthly_data['fecha'], 'y': monthly_data['ventas'], 'type': 'line'}],
        'layout': {'title': 'Ventas Mensuales'}
    }

    fig_segment = {}
    if segmento and 'producto' in df.columns:
        seg_data = df[df['producto'] == segmento]
        seg_summarized = seg_data.groupby('producto')['ventas'].sum().reset_index()
        fig_segment = {
            'data': [{'x': seg_summarized['producto'], 'y': seg_summarized['ventas'], 'type': 'bar'}],
            'layout': {'title': f'Ventas para {segmento}'}
        }

    return fig_monthly, fig_segment

@app.callback(
    Output('report-status', 'children'),
    Input('generate-report-button', 'n_clicks'),
    State('data-store', 'data')
)
def generate_report(n_clicks, data):
    if not n_clicks or data is None:
        return ""

    df = pd.DataFrame(data)
    # Calcular KPIs ejemplo:
    tsales = total_sales(df, 'ventas')
    kpis = {
        "Ventas Totales": tsales
    }

    # Opcional: generar un gráfico para el reporte (asumiendo ya lo generaste en un archivo)
    # plot_monthly_sales_trend(df, 'fecha', 'ventas', 'monthly_sales.png')

    # Generar el PDF
    generate_pdf_report("reporte.pdf", kpis, ["monthly_sales.png"])
    return "Reporte generado exitosamente: reporte.pdf"


if __name__ == "__main__":
    app.run_server(debug=True)
