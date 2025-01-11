# pip install holidays

import datetime
import holidays

def dias_uteis_no_mes(ano, mes, pais='BR'):
    feriados = holidays.CountryHoliday(pais, years=ano, subdiv='MG')

    feriados_bh = {
        datetime.date(ano, 8, 15): "Assunção de Nossa Senhora (feriado municipal)",
        datetime.date(ano, 12, 8): "Dia de Nossa Senhora da Conceição (feriado municipal)"
    }

    for data, nome in feriados_bh.items():
        feriados[data] = nome

    primeiro_dia = datetime.date(ano, mes, 1)
    if mes == 12:
        ultimo_dia = datetime.date(ano + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        ultimo_dia = datetime.date(ano, mes + 1, 1) - datetime.timedelta(days=1)

    dias_uteis = 0
    for dia in range((ultimo_dia - primeiro_dia).days + 1):
        dia_atual = primeiro_dia + datetime.timedelta(days=dia)
        if dia_atual.weekday() < 5 and dia_atual not in feriados:
            dias_uteis += 1

    return dias_uteis

def dias_uteis_por_ano(ano, pais='BR'):
    meses = [ "Janeiro" , "Fevereiro" , "Março" , "Abril" , "Maio" , "Junho" , "Julho" , "Agosto" , "Setembro" , "Outubro" , "Novembro" , "Dezembro" ]
    dias_uteis_meses = []

    for mes in range(1, 13):
        dias_uteis = dias_uteis_no_mes(ano, mes, pais)
        dias_uteis_meses.append((meses[mes - 1], dias_uteis))

    return dias_uteis_meses

ano = 2025
mes = 1
dias_uteis = dias_uteis_no_mes(ano, mes)
# print(f'O número de dias úteis em {mes}/{ano} é: {dias_uteis}')

dias_uteis_ano = dias_uteis_por_ano(ano)
for mes, dias_uteis in dias_uteis_ano:
    print(f'{mes}: {dias_uteis} dias úteis')