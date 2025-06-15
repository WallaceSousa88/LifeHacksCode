import re
import csv

from collections import defaultdict

# 1° Tratamento - Converter codificação para UTF-8
def convert_utf8(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as arquivo:
        conteudo = arquivo.read()
    with open(file_path, 'w', encoding='UTF-8') as arquivo:
        arquivo.write(conteudo)
    print(f"1 - Conversão para UTF-8 -> saida: '{file_path}'")

# 2° Tratamento - Remover espaço em branco maiores que 1
def rmv_space(file_path):
    special = re.compile(r'\s*([\/\\\?\-])\s*')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        linhas_processadas = []
        for ln in linhas:
            tmp = ' '.join(re.split(r'\s+', ln.strip()))
            tmp = special.sub(r'\1', tmp)
            linhas_processadas.append(tmp + '\n')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(linhas_processadas)

        print(f"2 - Remoção de espaços (>2) -> saída: '{file_path}'")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

# 3° Tratamento - TitleCase
def title_case(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')
            linhas = list(leitor)
        linhas_processadas = []
        for linha in linhas:
            linha_processada = [campo.strip().title() if campo else '' for campo in linha]
            linhas_processadas.append(linha_processada)
        with open(file_path, 'w', encoding='utf-8', newline='') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';', quoting=csv.QUOTE_ALL)
            escritor.writerows(linhas_processadas)
        print(f"3 - Padronização das palavras por TitleCase -> saida: '{file_path}'")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

# 4° Tratamento: Preposição, conjunção, artigo
def lowercase_words(file_path):
    palavras_para_ajustar = {
        'De': 'de' ,
        'Do': 'do' ,
        'Da': 'da' ,
        'Dos': 'dos' ,
        'Das': 'das' ,
        'E': 'e' ,
        'Em': 'em' ,
        'A': 'a' ,
        'As': 'as' ,
        'À': 'à' ,
        'Às': 'às' ,
        'Á': 'á' ,
        'Ás': 'ás' ,
        'Ao': 'ao' ,
        'O': 'o' ,
        'Ou': 'ou' ,
        'Os': 'os' ,
        'Que': 'que' ,
        'Um': 'um' ,
        'Uma': 'uma' ,
        'Uns': 'uns' ,
        'Umas': 'umas' ,
        'Para': 'para' ,
        'Por': 'por' ,
        'Como': 'como' ,
        'Com': 'com' ,
        'Se': 'se' ,
        'Mas': 'mas' ,
        'Ainda': 'ainda' ,
        'Embora': 'embora' ,
        'Nem': 'nem' ,
        'Logo': 'logo' ,
        'Pois': 'pois' ,
        'Porque': 'porque' ,
        'Portanto': 'portanto' ,
        'Contudo': 'contudo' ,
        'Todavia': 'todavia' ,
        'Entretanto': 'entretanto' ,
        'Além': 'além' ,
        'Apesar': 'apesar' ,
        'Conforme': 'conforme' ,
        'Desde': 'desde' ,
        'Depois': 'depois' ,
        'Durante': 'durante' ,
        'Até': 'até' ,
        'Entre': 'entre' ,
        'Sob': 'sob' ,
        'Sobre': 'sobre' ,
        'Contra': 'contra' ,
        'Sem': 'sem' ,
        'Mediante': 'mediante' ,
        'Segundo': 'segundo' ,
        'Atrás': 'atrás' ,
        'Diante': 'diante' ,
        'Perante': 'perante' ,
        'Trás': 'trás' ,
        'Já' : 'já' ,
        'Na' : 'na' ,
        'No' : 'no' ,
        'Fez' : 'fez' ,
        'Ser' : 'ser' ,
        'Desse' : 'desse'
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')
            linhas = list(leitor)
        linhas_ajustadas = []
        for linha in linhas:
            nova_linha = []
            for campo in linha:
                palavras = campo.strip().split()
                palavras_corrigidas = [
                    palavras_para_ajustar.get(palavra, palavra) for palavra in palavras
                ]
                nova_linha.append(' '.join(palavras_corrigidas))
            linhas_ajustadas.append(nova_linha)
        with open(file_path, 'w', encoding='utf-8', newline='') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';', quoting=csv.QUOTE_ALL)
            escritor.writerows(linhas_ajustadas)
        print(f"4 - Correção de preposição/conjunção -> saida: '{file_path}'")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

# Identificação dos itens para campos
def get_label(file_path):
    try:
        des_categoria = defaultdict(set)
        des_item = defaultdict(set)
        des_legenda = defaultdict(set)
        des_lista = defaultdict(set)

        with open(file_path, 'r', encoding='utf-8') as arquivo:
            leitor_csv = csv.reader(arquivo, delimiter=';')
            next(leitor_csv)

            for linha in leitor_csv:
                categoria = linha[2].strip()
                item = linha[3].strip()
                legenda = linha[4].strip()
                lista = linha[5].strip()

                des_categoria[categoria].add(item)
                des_item[item].add(legenda)
                des_legenda[legenda].add(lista)
                des_lista[lista].add((categoria, item, legenda))

        nome_arquivo_out = file_path.replace('.txt', '_out.txt')
        with open(nome_arquivo_out, 'w', encoding='utf-8') as arquivo_out:
            arquivo_out.write("Lista 1: DES_CATEGORIA\n")
            for categoria in sorted(des_categoria.keys()):
                arquivo_out.write(f"- {categoria}\n")

            arquivo_out.write("\nLista 2: DES_ITEM\n")
            for item in sorted(des_item.keys()):
                arquivo_out.write(f"- {item}\n")

            arquivo_out.write("\nCampos: DES_LEGENDA\n")
            for legenda in sorted(des_legenda.keys()):
                arquivo_out.write(f"- {legenda}\n")

        print(f"5 - Definição dos campos a serem criados -> saida: '{file_path}'")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

# Identificação dos itens para regras
def get_rules(file_path):
    item_legenda = defaultdict(set)
    legenda_item = defaultdict(set)

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            item = row[3].strip()
            legenda = row[4].strip()
            item_legenda[item].add(legenda)
            legenda_item[legenda].add(item)

    shared_items = set()
    for legenda, itens in legenda_item.items():
        if len(itens) > 1:
            shared_items |= itens

    output_file = file_path.replace('.txt', '_out_2.txt')
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("Mapa de DES_ITEM para DES_LEGENDA\n\n")
        for item in sorted(item_legenda):
            if item in shared_items:
                continue
            legendas = sorted(item_legenda[item])
            out.write(f"{item}\n")
            out.write(f"  - {', '.join(legendas)}\n\n")

        out.write("Legenda compartilhada por múltiplos itens\n\n")

        legenda_grupos = defaultdict(set)
        for legenda, itens in legenda_item.items():
            if len(itens) > 1:
                legenda_grupos[frozenset(itens)].add(legenda)

        for itens, legendas in sorted(legenda_grupos.items(), key=lambda x: sorted(x[0])):
            out.write(f"{', '.join(sorted(itens))}\n")
            out.write(f"  - {', '.join(sorted(legendas))}\n\n")

    print(f"6 - Definição das regras a serem criadas -> saida: '{output_file}'")
