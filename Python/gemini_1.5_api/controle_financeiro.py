import sqlite3
from datetime import datetime

def criar_banco():
    conexao = sqlite3.connect('despesas.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_compra DATE,
            data_pagamento DATE,
            valor REAL,
            descricao TEXT,
            origem TEXT,
            destino TEXT,
            valor_janis REAL,
            valor_wallace REAL
        )
    ''')

    conexao.commit()
    conexao.close()

def inserir_despesa(data_compra, data_pagamento, valor, descricao, origem, destino):
    conexao = sqlite3.connect('despesas.db')
    cursor = conexao.cursor()

    data_compra = datetime.strptime(data_compra, '%d-%m-%Y').strftime('%Y-%m-%d')
    data_pagamento = datetime.strptime(data_pagamento, '%d-%m-%Y').strftime('%Y-%m-%d')

    if origem == 'JANIS' and destino == 'JANIS':
        valor_janis = valor
        valor_wallace = 0
    elif origem == 'JANIS' and destino == 'WALLACE':
        valor_janis = 0
        valor_wallace = valor
    elif origem == 'JANIS' and destino == 'DIVIDIR':
        valor_janis = valor / 2
        valor_wallace = valor / 2
    elif origem == 'WALLACE' and destino == 'JANIS':
        valor_janis = valor
        valor_wallace = 0
    elif origem == 'WALLACE' and destino == 'WALLACE':
        valor_janis = 0
        valor_wallace = valor
    elif origem == 'WALLACE' and destino == 'DIVIDIR':
        valor_janis = valor / 2
        valor_wallace = valor / 2
    else:
        valor_janis = 0
        valor_wallace = 0

    cursor.execute('''
        INSERT INTO despesas (data_compra, data_pagamento, valor, descricao, origem, destino, valor_janis, valor_wallace)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data_compra, data_pagamento, valor, descricao, origem, destino, valor_janis, valor_wallace))

    conexao.commit()
    conexao.close()

def visualizar_despesas():
    conexao = sqlite3.connect('despesas.db')
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT * FROM despesas
    ''')

    for linha in cursor.fetchall():
        data_compra_formatada = datetime.strptime(linha[1], '%Y-%m-%d').strftime('%d-%m-%Y')
        data_pagamento_formatada = datetime.strptime(linha[2], '%Y-%m-%d').strftime('%d-%m-%Y')
        
        print(f"ID: {linha[0]}, Data da Compra: {data_compra_formatada}, Data do Pagamento: {data_pagamento_formatada}, Valor: {linha[3]}, Descrição: {linha[4]}, Origem: {linha[5]}, Destino: {linha[6]}, Valor Janis: {linha[7]}, Valor Wallace: {linha[8]}")
    
    conexao.close()

criar_banco()

while True:
    print("\nControle de Despesas:")
    print("1. Inserir Despesa")
    print("2. Visualizar Despesas")
    print("3. Sair")

    opcao = input("ESCOLHA UMA OPCAO: ")

    if opcao == '1':
        data_compra = input("DATA COMPRA (DD-MM-YYYY): ")
        data_pagamento = input("DATA PAGAMENTO (DD-MM-YYYY): ")
        valor = float(input("VALOR: "))
        descricao = input("DESCRICAO: ")
        origem = input("ORIGEM (JANIS / WALLACE): ").upper()
        destino = input("DESTINO (JANIS / WALLACE / DIVIDIR): ").upper()

        inserir_despesa(data_compra, data_pagamento, valor, descricao, origem, destino)
        print("DESPESA INSERIDA COM SUCESSO!")

    elif opcao == '2':
        visualizar_despesas()

    elif opcao == '3':
        break

    else:
        print("OPCAO INVALIDA!")