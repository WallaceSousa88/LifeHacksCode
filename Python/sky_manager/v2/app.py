# pip install flask dash pandas openpyxl plotly

import os
import time
import pandas as pd
from flask import Flask
from dash import Dash, dcc, html, dash_table, Input, Output

EXCEL_PATH = "data.xlsx"
SHEET_NAME = "Planilha1"
REFRESH_SECONDS = 30

def read_excel():
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
    df.columns = [str(c).strip().upper() for c in df.columns]
    if "DATA" in df.columns:
        df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=False)
    for col in ["QUANTIDADE","PRECO UNIT.","PRECO TOTAL","DIAMETRO CABECA (MM)","DIAMETRO ROSCA (MM)","COMPRIMENTO ROSCA (MM)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

server = Flask(__name__)
dash_app = Dash(__name__, server=server, url_base_pathname='/')

dash_app.layout = html.Div([
    html.H2("Dashboard de Almoxarifado — Planilha1"),
    html.Div("Dados lidos dinamicamente do Excel. Salve a planilha para refletir aqui."),
    dcc.Interval(id='interval', interval=REFRESH_SECONDS*1000, n_intervals=0),

    html.H4("Filtros"),
    html.Div([
        dcc.Dropdown(id='desc', placeholder='DESCRICAO', multi=True),
        dcc.Dropdown(id='tipo', placeholder='CATEGORIA / TIPO', multi=True),
        dcc.Dropdown(id='mat', placeholder='MATERIAL', multi=True),
        dcc.Dropdown(id='forn', placeholder='FORNECEDOR', multi=True)
    ], style={'display':'grid','gridTemplateColumns':'1fr 1fr 1fr 1fr','gap':'10px'}),

    html.H4("Tabela"),
    dcc.Dropdown(id='columns', multi=True, placeholder='Escolha colunas para exibir'),
    dash_table.DataTable(id='table', page_size=20, filter_action='native', sort_action='native', style_table={'overflowX':'auto'}),

    html.H4("Gráfico"),
    html.Div([
        dcc.Dropdown(id='x_dim', placeholder='Dimensão (X)', multi=False),
        dcc.Dropdown(id='y_metric', placeholder='Métrica (Y)', multi=False),
        dcc.Slider(id='topn', min=5, max=50, step=1, value=15)
    ], style={'display':'grid','gridTemplateColumns':'1fr 1fr 1fr','gap':'10px'}),
    dcc.Graph(id='bar')
])

@dash_app.callback(
    [Output('desc','options'), Output('tipo','options'), Output('mat','options'), Output('forn','options'),
     Output('columns','options'), Output('x_dim','options'), Output('y_metric','options'),
     Output('table','columns')],
    Input('interval','n_intervals')
)
def refresh_options(_):
    df = read_excel()
    def opts(col):
        return [{'label': str(x), 'value': str(x)} for x in sorted(df[col].dropna().astype(str).unique())] if col in df.columns else []
    columns = [{'name': c, 'id': c} for c in df.columns]
    x_dim = [{'label': c, 'value': c} for c in df.columns if df[c].dtype == 'object']
    y_metric = [{'label': c, 'value': c} for c in ["QUANTIDADE","PRECO TOTAL","PRECO UNIT."] if c in df.columns]
    return opts("DESCRICAO"), opts("CATEGORIA / TIPO"), opts("MATERIAL"), opts("FORNECEDOR"), \
           [{'label': c, 'value': c} for c in df.columns], x_dim, y_metric, columns

@dash_app.callback(
    [Output('table','data'), Output('bar','figure')],
    [Input('interval','n_intervals'),
     Input('desc','value'), Input('tipo','value'), Input('mat','value'), Input('forn','value'),
     Input('columns','value'), Input('x_dim','value'), Input('y_metric','value'), Input('topn','value')]
)
def update_view(_, desc, tipo, mat, forn, cols, x_dim, y_metric, topn):
    df = read_excel()
    # aplica filtros
    def apply_filter(col, vals):
        nonlocal df
        if col in df.columns and vals:
            df = df[df[col].astype(str).isin(vals)]
    apply_filter("DESCRICAO", desc)
    apply_filter("CATEGORIA / TIPO", tipo)
    apply_filter("MATERIAL", mat)
    apply_filter("FORNECEDOR", forn)

    data = df[cols] if cols else df
    # gráfico
    import plotly.express as px
    if x_dim and y_metric and x_dim in df.columns and y_metric in df.columns:
        grp = df.groupby(x_dim, dropna=False)[y_metric].sum().sort_values(ascending=False).head(topn).reset_index()
        fig = px.bar(grp, x=x_dim, y=y_metric, title=f"Top {topn} por {x_dim}", text=y_metric)
        fig.update_layout(margin=dict(l=0,r=0,t=40,b=0))
    else:
        fig = px.bar(pd.DataFrame({"INFO":["Selecione X e Y"],"VALOR":[0]}), x="INFO", y="VALOR", title="Selecione dimensões")
    return data.to_dict('records'), fig

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))