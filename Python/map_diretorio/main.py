import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class MapeadorDiretoriosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapeador de Diretórios")
        self.root.geometry("315x230")
        self.centralizar_janela(self.root, 315, 230)

        tk.Label(self.root, text="Perfil Rápido (Opcional):").pack(pady=(10, 0))
        self.combo_perfil = ttk.Combobox(self.root, state="readonly", width=30)
        self.perfis = {
            "Personalizado / Todos os Arquivos": "",
            "Web (.html .css .js .ts)": ".html .css .js .ts .tsx",
            "Python (.py .ipynb)": ".py .ipynb",
            "Data Science (.csv .json .py)": ".csv .json .py",
            "C/C++ (.c .cpp .h)": ".c .cpp .h .hpp"
        }
        self.combo_perfil['values'] = list(self.perfis.keys())
        self.combo_perfil.current(0)
        self.combo_perfil.pack(pady=5)
        self.combo_perfil.bind("<<ComboboxSelected>>", self.aplicar_perfil)

        tk.Label(self.root, text="Extensões (separadas por espaço):").pack(pady=5)
        self.entrada_extensoes = tk.Entry(self.root, width=32)
        self.entrada_extensoes.pack(pady=5)

        self.botao_selecionar = tk.Button(self.root, text="Selecionar Diretório", command=self.selecionar_diretorio)
        self.botao_selecionar.pack(pady=15)

    def aplicar_perfil(self, event=None):
        selecao = self.combo_perfil.get()
        extensoes = self.perfis.get(selecao, "")
        self.entrada_extensoes.delete(0, tk.END)
        self.entrada_extensoes.insert(0, extensoes)

    def centralizar_janela(self, janela, largura, altura):
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        janela.geometry(f'{largura}x{altura}+{x}+{y}')

    def listar_arquivos(self, caminho, extensoes=None):
        if extensoes:
            extensoes = [ext if ext.startswith('.') else f'.{ext}' for ext in extensoes]

        pastas_ignoradas = {'.git', 'venv', 'node_modules', '__pycache__', '.vscode', '.idea', 'dist', 'build', 'env'}

        for root_dir, dirs, files in os.walk(caminho):
            dirs[:] = [d for d in dirs if d not in pastas_ignoradas]

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

    def gerar_texto_final(self, itens_selecionados, caminho_base):
        texto = []
        texto.append("Abaixo está a estrutura de diretórios e a lista dos arquivos, seguida pelos conteúdos de cada arquivo:\n\n")

        texto.append("--- Estrutura de Diretórios ---\n")
        nome_pasta_base = os.path.basename(caminho_base) or caminho_base
        texto.append(f"{nome_pasta_base}/\n")
        arvore_texto = self.gerar_arvore_arquivos(itens_selecionados, caminho_base)
        if arvore_texto:
            texto.append(arvore_texto + "\n")
        texto.append("-------------------------------\n\n")

        for arquivo in itens_selecionados:
            nome_do_arquivo = os.path.relpath(arquivo, caminho_base)
            texto.append(f"--- Início do arquivo: {nome_do_arquivo} ---\n")
            try:
                with open(arquivo, 'r', encoding='utf-8') as file_content:
                    texto.append(file_content.read() + '\n')
            except UnicodeDecodeError:
                texto.append(f"--- Erro: Arquivo ignorado (parece ser binário ou tem codificação não suportada) ---\n")
            except Exception as e:
                texto.append(f"Erro ao ler o arquivo: {e}\n")
            texto.append(f"--- Fim do arquivo: {nome_do_arquivo} ---\n\n")

        return "".join(texto)

    def salvar_em_txt(self, caminho_destino, itens_selecionados, caminho_base):
        try:
            texto_final = self.gerar_texto_final(itens_selecionados, caminho_base)
            with open(caminho_destino, 'w', encoding='utf-8') as f:
                f.write(texto_final)
            messagebox.showinfo("Sucesso", f"Lista de arquivos salva com sucesso em:\n{caminho_destino}")
            self.root.quit()
        except PermissionError:
            messagebox.showerror("Erro", f"Permissão negada para escrever em: {caminho_destino}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

    def copiar_para_area_transferencia(self, itens_selecionados, caminho_base):
        try:
            texto_final = self.gerar_texto_final(itens_selecionados, caminho_base)
            self.root.clipboard_clear()
            self.root.clipboard_append(texto_final)
            messagebox.showinfo("Sucesso", "Conteúdo copiado para a Área de Transferência com sucesso!")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar: {e}")

    def selecionar_diretorio(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.listar_itens(caminho)

    def listar_itens(self, caminho):
        janela_itens = tk.Toplevel(self.root)
        janela_itens.title("Selecionar Itens")
        janela_itens.geometry("500x500")
        self.centralizar_janela(janela_itens, 500, 500)
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
            try:
                tamanho_kb = os.path.getsize(item) / 1024
                lista.insert(tk.END, f"{rel_path} ({tamanho_kb:.1f} KB)")
            except Exception:
                lista.insert(tk.END, f"{rel_path} (Erro ao ler tamanho)")
        lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lista.yview)

        frame_botoes_selecao = tk.Frame(janela_itens)
        frame_botoes_selecao.pack(fill=tk.X, padx=10)

        label_tamanho = tk.Label(janela_itens, text="Tamanho Total Selecionado: 0.0 KB", font=("Arial", 9, "bold"))
        label_tamanho.pack(pady=5)

        def atualizar_tamanho(event=None):
            tamanho_total = 0
            for index in lista.curselection():
                try:
                    tamanho_total += os.path.getsize(itens[index])
                except Exception:
                    pass
            tamanho_kb = tamanho_total / 1024
            if tamanho_kb > 1024:
                tamanho_mb = tamanho_kb / 1024
                label_tamanho.config(text=f"Tamanho Total Selecionado: {tamanho_mb:.2f} MB")
            else:
                label_tamanho.config(text=f"Tamanho Total Selecionado: {tamanho_kb:.1f} KB")

        lista.bind('<<ListboxSelect>>', atualizar_tamanho)

        def selecionar_tudo():
            lista.select_set(0, tk.END)
            atualizar_tamanho()

        def desmarcar_tudo():
            lista.selection_clear(0, tk.END)
            atualizar_tamanho()

        tk.Button(frame_botoes_selecao, text="Selecionar Tudo", command=selecionar_tudo).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(frame_botoes_selecao, text="Desmarcar Tudo", command=desmarcar_tudo).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        def get_itens_selecionados():
            if not lista.curselection():
                messagebox.showwarning("Aviso", "Por favor, selecione ao menos um arquivo.")
                return None
            itens_selecionados = []
            for index in lista.curselection():
                itens_selecionados.append(itens[index])
            return itens_selecionados

        def marcar_item():
            itens_selecionados = get_itens_selecionados()
            if not itens_selecionados:
                return

            nome_sugerido = os.path.basename(caminho) + '.txt'
            arquivo_destino = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=nome_sugerido,
                title="Salvar arquivo de saída",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if arquivo_destino:
                self.salvar_em_txt(arquivo_destino, itens_selecionados, caminho)

        def copiar_itens():
            itens_selecionados = get_itens_selecionados()
            if not itens_selecionados:
                return
            self.copiar_para_area_transferencia(itens_selecionados, caminho)

        frame_acoes = tk.Frame(janela_itens)
        frame_acoes.pack(pady=10)

        botao_salvar = tk.Button(frame_acoes, text="Salvar em .txt", command=marcar_item)
        botao_salvar.pack(side=tk.LEFT, padx=10)

        botao_copiar = tk.Button(frame_acoes, text="Copiar para Área de Transferência", command=copiar_itens)
        botao_copiar.pack(side=tk.LEFT, padx=10)

def main():
    root = tk.Tk()
    app = MapeadorDiretoriosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()