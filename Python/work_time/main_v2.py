# pip install pandas reportlab pdfplumber

import os
import pandas as pd
import pdfplumber

from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def calcular_horas(planilha):
    horario_padrao = timedelta(hours=8, minutes=13)
    horas_excedentes = []
    horas_a_cumprir = []
    for _, linha in planilha.iterrows():
        entrada1 = datetime.strptime(str(linha['Entrada1']), '%H:%M:%S')
        saida1 = datetime.strptime(str(linha['Saida1']), '%H:%M:%S')
        entrada2 = datetime.strptime(str(linha['Entrada2']), '%H:%M:%S')
        saida2 = datetime.strptime(str(linha['Saida2']), '%H:%M:%S')
        tempo_trabalhado = (saida1 - entrada1) + (saida2 - entrada2)
        if tempo_trabalhado > horario_padrao:
            horas_excedentes.append(tempo_trabalhado - horario_padrao)
            horas_a_cumprir.append(timedelta(0))
        else:
            horas_excedentes.append(timedelta(0))
            horas_a_cumprir.append(horario_padrao - tempo_trabalhado)
    planilha['Horas Excedentes'] = horas_excedentes
    planilha['Horas a Cumprir'] = horas_a_cumprir
    return planilha

def formatar_timedelta(td):
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days} days {hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:02}"

def extrair_tabelas_pdf(caminho_pdf):
    tabelas = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            tabelas_pagina = pagina.extract_tables()
            for tabela in tabelas_pagina:
                df = pd.DataFrame(tabela[1:], columns=tabela[0])
                if 'Entrada1' in df.columns and 'Saida1' in df.columns:
                    tabelas.append(df)
    return tabelas

def calcular_totais(planilha):
    total_excedentes = sum(planilha['Horas Excedentes'], timedelta())
    total_a_cumprir = sum(planilha['Horas a Cumprir'], timedelta())
    diferenca = abs(total_excedentes - total_a_cumprir)
    status = "Sobrando" if total_excedentes > total_a_cumprir else "Devendo"
    return formatar_timedelta(total_excedentes), formatar_timedelta(total_a_cumprir), f"{formatar_timedelta(diferenca)} ({status})"

pasta_entrada = 'entrada'
pasta_saida = 'saida'

if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

dados_pdf = []

for nome_arquivo in os.listdir(pasta_entrada):
    if nome_arquivo.endswith('.pdf'):
        caminho_completo_arquivo = os.path.join(pasta_entrada, nome_arquivo)
        tabelas = extrair_tabelas_pdf(caminho_completo_arquivo)
        for i, planilha in enumerate(tabelas):
            if not planilha.empty:
                planilha['Data'] = pd.to_datetime(planilha['Data']).dt.strftime('%d/%m/%Y')
                planilha = calcular_horas(planilha)

                total_excedentes, total_a_cumprir, diferenca = calcular_totais(planilha)

                dados_pdf.append({
                    'nome': f"{os.path.splitext(nome_arquivo)[0]}_pagina_{i+1}",
                    'tabela': planilha.values.tolist(),
                    'cabecalho': list(planilha.columns),
                    'totais': [total_excedentes, total_a_cumprir, diferenca]
                })

doc = SimpleDocTemplate(os.path.join(pasta_saida, "relatorio_completo.pdf"), pagesize=letter)
elementos = []
styles = getSampleStyleSheet()

dados_pdf.sort(key=lambda x: x['nome'])

for dados in dados_pdf:
    elementos.append(Paragraph(dados['nome'], styles['Heading1']))
    elementos.append(Spacer(1, 12))
    tabela = Table(
        [dados['cabecalho']] + dados['tabela'],
        style=[
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)
        ]
    )
    elementos.append(tabela)
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("Calculado pelo Python", styles['Normal']))
    elementos.append(Paragraph(f"Total Horas Excedentes: {dados['totais'][0]}", styles['Normal']))
    elementos.append(Paragraph(f"Total Horas a Cumprir: {dados['totais'][1]}", styles['Normal']))
    elementos.append(Paragraph(f"Diferença: {dados['totais'][2]}", styles['Normal']))
    elementos.append(PageBreak())

doc.build(elementos)
print("Calculo concluido e resultados salvos na pasta 'saida'.")
