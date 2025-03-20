import os
import tkinter as tk

from tkinter import filedialog, messagebox

def listar_arquivos(caminho, extensoes=None):
    for root, dirs, files in os.walk(caminho):
        for file in files:
            if not extensoes or any(file.endswith(ext) for ext in extensoes):
                yield os.path.join(root, file)

def salvar_em_txt(caminho, itens_selecionados):
    nome_arquivo = os.path.basename(caminho) + '.txt'
    caminho_area_trabalho = os.path.join(os.path.expanduser("~"), "Desktop", nome_arquivo)
    try:
        with open(caminho_area_trabalho, 'w', encoding='utf-8') as f:
            f.write("Abaixo está a lista dos arquivos neste diretório, seguida pelos conteúdos de cada arquivo:\n\n")
            for arquivo in itens_selecionados:
                nome_do_arquivo = os.path.basename(arquivo)
                f.write(f"--- Início do arquivo: {nome_do_arquivo} ---\n")
                try:
                    with open(arquivo, 'r', encoding='utf-8') as file_content:
                        f.write(file_content.read() + '\n')
                except Exception as e:
                    f.write(f"Erro ao ler o arquivo: {e}\n")
                f.write(f"--- Fim do arquivo: {nome_do_arquivo} ---\n\n")
        messagebox.showinfo("Sucesso", f"Lista de arquivos e seus conteúdos salva em: {caminho_area_trabalho}")
        root.quit()
    except PermissionError:
        messagebox.showerror("Erro", f"Permissão negada para escrever em: {caminho_area_trabalho}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

def selecionar_diretorio():
    caminho = filedialog.askdirectory()
    if caminho:
        listar_itens(caminho)

def listar_itens(caminho):
    janela_itens = tk.Toplevel()
    janela_itens.title("Selecionar Itens")
    janela_itens.geometry("400x300")
    centralizar_janela(janela_itens, 400, 300)
    janela_itens.transient(root)

    extensoes = entrada_extensoes.get().split()
    itens = list(listar_arquivos(caminho, extensoes))
    itens_selecionados = []

    def marcar_item():
        itens_selecionados.clear()
        for item in lista.curselection():
            itens_selecionados.append(lista.get(item))
        salvar_em_txt(caminho, itens_selecionados)

    lista = tk.Listbox(janela_itens, selectmode=tk.MULTIPLE)
    for item in itens:
        lista.insert(tk.END, item)
    lista.pack(fill=tk.BOTH, expand=True)

    botao_salvar = tk.Button(janela_itens, text="Salvar", command=marcar_item)
    botao_salvar.pack(pady=10)

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f'{largura}x{altura}+{x}+{y}')

def main():
    global root, entrada_extensoes
    root = tk.Tk()
    root.title("Mapeador de Diretórios")
    root.geometry("315x170")
    centralizar_janela(root, 315, 170)

    tk.Label(root, text="Extensões (separadas por espaço):").pack(pady=5)
    entrada_extensoes = tk.Entry(root)
    entrada_extensoes.pack(pady=5)

    botao_selecionar = tk.Button(root, text="Selecionar Diretório", command=selecionar_diretorio)
    botao_selecionar.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()