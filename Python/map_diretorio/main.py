import os
import tkinter as tk
from tkinter import filedialog, messagebox

class MapeadorDiretoriosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapeador de Diretórios")
        self.root.geometry("315x170")
        self.centralizar_janela(self.root, 315, 170)

        tk.Label(self.root, text="Extensões (separadas por espaço):").pack(pady=5)
        self.entrada_extensoes = tk.Entry(self.root)
        self.entrada_extensoes.pack(pady=5)

        self.botao_selecionar = tk.Button(self.root, text="Selecionar Diretório", command=self.selecionar_diretorio)
        self.botao_selecionar.pack(pady=20)

    def centralizar_janela(self, janela, largura, altura):
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        janela.geometry(f'{largura}x{altura}+{x}+{y}')

    def listar_arquivos(self, caminho, extensoes=None):
        if extensoes:
            extensoes = [ext if ext.startswith('.') else f'.{ext}' for ext in extensoes]
        for root_dir, dirs, files in os.walk(caminho):
            for file in files:
                if not extensoes or any(file.endswith(ext) for ext in extensoes):
                    yield os.path.join(root_dir, file)

    def gerar_arvore_arquivos(self, itens_selecionados, caminho_base):
        arvore = {}
        for arquivo in itens_selecionados:
            rel_path = os.path.relpath(arquivo, caminho_base)
            partes = rel_path.split(os.sep)
            atual = arvore
            for parte in partes:
                if parte not in atual:
                    atual[parte] = {}
                atual = atual[parte]

        linhas_arvore = []
        def formatar_arvore(no, prefixo=""):
            chaves = list(no.keys())
            chaves.sort()
            for i, chave in enumerate(chaves):
                is_last = (i == len(chaves) - 1)
                conector = "└── " if is_last else "├── "
                linhas_arvore.append(f"{prefixo}{conector}{chave}")
                filhos = no[chave]
                if filhos:
                    novo_prefixo = prefixo + ("    " if is_last else "│   ")
                    formatar_arvore(filhos, novo_prefixo)
                    
        formatar_arvore(arvore)
        return "\n".join(linhas_arvore)

    def salvar_em_txt(self, caminho_destino, itens_selecionados, caminho_base):
        try:
            with open(caminho_destino, 'w', encoding='utf-8') as f:
                f.write("Abaixo está a estrutura de diretórios e a lista dos arquivos, seguida pelos conteúdos de cada arquivo:\n\n")
                
                f.write("--- Estrutura de Diretórios ---\n")
                nome_pasta_base = os.path.basename(caminho_base) or caminho_base
                f.write(f"{nome_pasta_base}/\n")
                arvore_texto = self.gerar_arvore_arquivos(itens_selecionados, caminho_base)
                if arvore_texto:
                    f.write(arvore_texto + "\n")
                f.write("-------------------------------\n\n")

                for arquivo in itens_selecionados:
                    nome_do_arquivo = os.path.relpath(arquivo, caminho_base)
                    f.write(f"--- Início do arquivo: {nome_do_arquivo} ---\n")
                    try:
                        with open(arquivo, 'r', encoding='utf-8') as file_content:
                            f.write(file_content.read() + '\n')
                    except UnicodeDecodeError:
                        f.write(f"--- Erro: Arquivo ignorado (parece ser binário ou tem codificação não suportada) ---\n")
                    except Exception as e:
                        f.write(f"Erro ao ler o arquivo: {e}\n")
                    f.write(f"--- Fim do arquivo: {nome_do_arquivo} ---\n\n")
            messagebox.showinfo("Sucesso", f"Lista de arquivos salva com sucesso em:\n{caminho_destino}")
            self.root.quit()
        except PermissionError:
            messagebox.showerror("Erro", f"Permissão negada para escrever em: {caminho_destino}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

    def selecionar_diretorio(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.listar_itens(caminho)

    def listar_itens(self, caminho):
        janela_itens = tk.Toplevel(self.root)
        janela_itens.title("Selecionar Itens")
        janela_itens.geometry("400x400")
        self.centralizar_janela(janela_itens, 400, 400)
        janela_itens.transient(self.root)

        extensoes = self.entrada_extensoes.get().split()
        itens = list(self.listar_arquivos(caminho, extensoes))
        
        frame_lista = tk.Frame(janela_itens)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        lista = tk.Listbox(frame_lista, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        for item in itens:
            rel_path = os.path.relpath(item, caminho)
            lista.insert(tk.END, rel_path)
        lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lista.yview)

        frame_botoes_selecao = tk.Frame(janela_itens)
        frame_botoes_selecao.pack(fill=tk.X, padx=10)

        def selecionar_tudo():
            lista.select_set(0, tk.END)

        def desmarcar_tudo():
            lista.selection_clear(0, tk.END)

        tk.Button(frame_botoes_selecao, text="Selecionar Tudo", command=selecionar_tudo).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(frame_botoes_selecao, text="Desmarcar Tudo", command=desmarcar_tudo).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        def marcar_item():
            if not lista.curselection():
                messagebox.showwarning("Aviso", "Por favor, selecione ao menos um arquivo.")
                return

            itens_selecionados = []
            for index in lista.curselection():
                caminho_completo = os.path.join(caminho, lista.get(index))
                itens_selecionados.append(caminho_completo)

            nome_sugerido = os.path.basename(caminho) + '.txt'
            arquivo_destino = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=nome_sugerido,
                title="Salvar arquivo de saída",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if arquivo_destino:
                self.salvar_em_txt(arquivo_destino, itens_selecionados, caminho)

        botao_salvar = tk.Button(janela_itens, text="Salvar", command=marcar_item)
        botao_salvar.pack(pady=10)

def main():
    root = tk.Tk()
    app = MapeadorDiretoriosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()