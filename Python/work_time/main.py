# pip install pandas openpyxl reportlab tabulate

import pandas as pd
import os

from datetime import datetime, timedelta
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
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
    planilha['HoraExtra'] = [str(h).split('.')[0] for h in horas_excedentes]
    planilha['HorasDevidas'] = [str(h).split('.')[0] for h in horas_a_cumprir]
    return planilha, horas_excedentes, horas_a_cumprir

def somar_horas(horas):
    total = timedelta()
    for h in horas:
        total += h
    return total

pasta_entrada = 'entrada'
pasta_saida = 'saida'
relatorio_resumo = []

if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

dados_pdf = []

for nome_arquivo in os.listdir(pasta_entrada):
    if nome_arquivo.endswith('.xlsx'):
        caminho_completo_arquivo = os.path.join(pasta_entrada, nome_arquivo)
        planilha = pd.read_excel(caminho_completo_arquivo, usecols='A,B,C,D,E')
        planilha['Data'] = pd.to_datetime(planilha['Data']).dt.strftime('%d/%m/%Y')
        planilha, horas_excedentes, horas_a_cumprir = calcular_horas(planilha)
        total_horas_excedentes = somar_horas(horas_excedentes)
        total_horas_a_cumprir = somar_horas(horas_a_cumprir)

        if total_horas_excedentes > total_horas_a_cumprir:
            situacao_horas = "O funcionario tem horas a mais"
            diferenca_horas = total_horas_excedentes - total_horas_a_cumprir
        else:
            situacao_horas = "O funcionario deve horas"
            diferenca_horas = total_horas_a_cumprir - total_horas_excedentes

        diferenca_horas_str = str(diferenca_horas).split('.')[0]

        nome_base_arquivo = os.path.splitext(nome_arquivo)[0]
        relatorio_resumo.append(f"{nome_base_arquivo}: {situacao_horas}, {diferenca_horas_str}")
        nome_arquivo_saida = f"resultado_{nome_base_arquivo}.txt"
        caminho_completo_saida = os.path.join(pasta_saida, nome_arquivo_saida)

        with open(caminho_completo_saida, 'w') as arquivo_saida:
            arquivo_saida.write(tabulate(planilha, headers='keys', tablefmt='grid', showindex=False))
            arquivo_saida.write(f"\n\nTotal de Horas Extras: {total_horas_excedentes}\n")
            arquivo_saida.write(f"Total de Horas Devidas: {total_horas_a_cumprir}\n")
            arquivo_saida.write(f"Diferenca: {situacao_horas}, {diferenca_horas_str}\n")

        dados_pdf.append({
            'nome': nome_base_arquivo,
            'tabela': planilha.values.tolist(),
            'cabecalho': list(planilha.columns),
            'total_horas_excedentes': total_horas_excedentes,
            'total_horas_a_cumprir': total_horas_a_cumprir,
            'situacao_horas': situacao_horas,
            'diferenca_horas_str': diferenca_horas_str
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
    elementos.append(Paragraph(f"Total de Horas Extras: {dados['total_horas_excedentes']}", styles['Normal']))
    elementos.append(Paragraph(f"Total de Horas Devidas: {dados['total_horas_a_cumprir']}", styles['Normal']))
    elementos.append(Paragraph(f"Diferenca: {dados['situacao_horas']}, {dados['diferenca_horas_str']}", styles['Normal']))
    elementos.append(PageBreak())

doc.build(elementos)

with open(os.path.join(pasta_saida, 'resumo.txt'), 'w') as arquivo_saida:
    for linha in sorted(relatorio_resumo):
        arquivo_saida.write(linha + '\n')

print("Calculo concluido e resultados salvos na pasta 'saida'.")
