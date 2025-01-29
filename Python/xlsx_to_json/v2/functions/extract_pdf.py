import os
import pdfplumber

def extract_pdf(pasta_entrada, pasta_saida):
    def extract_data(caminho_pdf):
        with pdfplumber.open(caminho_pdf) as pdf:
            texto_formatado = ""
            for pagina in pdf.pages:
                tabelas = pagina.extract_tables()
                for tabela in tabelas:
                    for linha in tabela:
                        linha = [str(item) if item is not None else '' for item in linha]
                        linha_formatada = ";".join(linha)
                        texto_formatado += linha_formatada + "\n"
        return texto_formatado

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    for nome_arquivo in os.listdir(pasta_entrada):
        if nome_arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(pasta_entrada, nome_arquivo)
            dados_extraidos = extract_data(caminho_pdf)

            caminho_saida = os.path.join(pasta_saida, nome_arquivo.replace(".pdf", ".csv"))

            with open(caminho_saida, 'w', encoding='utf-8') as f:
                f.write(dados_extraidos)

if __name__ == "__main__":
    pasta_entrada = os.path.join(os.path.dirname(__file__), '..', 'in')
    pasta_saida = os.path.join(os.path.dirname(__file__), '..', 'out')
    extract_pdf(pasta_entrada, pasta_saida)