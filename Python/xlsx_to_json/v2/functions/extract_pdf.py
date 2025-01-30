import os
import pdfplumber
import shutil

def extract_pdf(input_folder, output_folder):
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

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    for nome_arquivo in os.listdir(input_folder):
        if nome_arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(input_folder, nome_arquivo)
            dados_extraidos = extract_data(caminho_pdf)

            caminho_saida = os.path.join(output_folder, nome_arquivo.replace(".pdf", ".csv"))

            with open(caminho_saida, 'w', encoding='utf-8') as f:
                f.write(dados_extraidos)

if __name__ == "__main__":
    input_folder = os.path.join(os.path.dirname(__file__), '..', 'in')
    output_folder = os.path.join(os.path.dirname(__file__), '..', 'out')
    extract_pdf(input_folder, output_folder)