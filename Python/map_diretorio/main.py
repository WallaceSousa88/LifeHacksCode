import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MapeadorDiretoriosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapeador de Diretórios")
        self.root.geometry("400x280")
        self.centralizar_janela(self.root, 400, 280)

        customtkinter.CTkLabel(self.root, text="Perfil Rápido (Opcional):", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        
        self.perfis = {
            "Personalizado / Todos os Arquivos": "",
            "Web (.html .css .js .ts)": ".html .css .js .ts .tsx",
            "Python (.py .ipynb)": ".py .ipynb",
            "Data Science (.csv .json .py)": ".csv .json .py",
            "C/C++ (.c .cpp .h)": ".c .cpp .h .hpp"
        }
        self.combo_perfil = customtkinter.CTkComboBox(self.root, values=list(self.perfis.keys()), state="readonly", width=300, command=self.aplicar_perfil)
        self.combo_perfil.set("Personalizado / Todos os Arquivos")
        self.combo_perfil.pack(pady=5)

        customtkinter.CTkLabel(self.root, text="Extensões (separadas por espaço):", font=("Roboto", 14, "bold")).pack(pady=(10, 5))
        self.entrada_extensoes = customtkinter.CTkEntry(self.root, width=300)
        self.entrada_extensoes.pack(pady=5)

        self.botao_selecionar = customtkinter.CTkButton(self.root, text="Selecionar Diretório", command=self.selecionar_diretorio, height=40)
        self.botao_selecionar.pack(pady=20)

    def aplicar_perfil(self, selecao):
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
        janela_itens = customtkinter.CTkToplevel(self.root)
        janela_itens.title("Selecionar Itens")
        janela_itens.geometry("600x550")
        self.centralizar_janela(janela_itens, 600, 550)
        janela_itens.transient(self.root)
        janela_itens.grab_set()

        extensoes = self.entrada_extensoes.get().split()
        itens = list(self.listar_arquivos(caminho, extensoes))

        scrollable_frame = customtkinter.CTkScrollableFrame(janela_itens, label_text="Arquivos Encontrados")
        scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        label_tamanho = customtkinter.CTkLabel(janela_itens, text="Tamanho Total Selecionado: 0.0 KB", font=("Roboto", 14, "bold"))
        label_tamanho.pack(pady=5)

        self.checkboxes = []

        def atualizar_tamanho():
            tamanho_total = 0
            for cb, item_path in self.checkboxes:
                if cb.get() == 1:
                    try:
                        tamanho_total += os.path.getsize(item_path)
                    except Exception:
                        pass
            tamanho_kb = tamanho_total / 1024
            if tamanho_kb > 1024:
                tamanho_mb = tamanho_kb / 1024
                label_tamanho.configure(text=f"Tamanho Total Selecionado: {tamanho_mb:.2f} MB")
            else:
                label_tamanho.configure(text=f"Tamanho Total Selecionado: {tamanho_kb:.1f} KB")

        for item in itens:
            rel_path = os.path.relpath(item, caminho)
            try:
                tamanho_kb = os.path.getsize(item) / 1024
                texto_cb = f"{rel_path} ({tamanho_kb:.1f} KB)"
            except Exception:
                texto_cb = f"{rel_path} (Erro ao ler tamanho)"
            
            cb = customtkinter.CTkCheckBox(scrollable_frame, text=texto_cb, command=atualizar_tamanho)
            cb.pack(anchor="w", pady=5, padx=10)
            self.checkboxes.append((cb, item))

        frame_botoes_selecao = customtkinter.CTkFrame(janela_itens, fg_color="transparent")
        frame_botoes_selecao.pack(fill=tk.X, padx=20, pady=5)

        def selecionar_tudo():
            for cb, _ in self.checkboxes:
                cb.select()
            atualizar_tamanho()

        def desmarcar_tudo():
            for cb, _ in self.checkboxes:
                cb.deselect()
            atualizar_tamanho()

        customtkinter.CTkButton(frame_botoes_selecao, text="Selecionar Tudo", command=selecionar_tudo, fg_color="gray").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        customtkinter.CTkButton(frame_botoes_selecao, text="Desmarcar Tudo", command=desmarcar_tudo, fg_color="gray").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        def get_itens_selecionados():
            itens_selecionados = [item_path for cb, item_path in self.checkboxes if cb.get() == 1]
            if not itens_selecionados:
                messagebox.showwarning("Aviso", "Por favor, selecione ao menos um arquivo.")
                return None
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

        frame_acoes = customtkinter.CTkFrame(janela_itens, fg_color="transparent")
        frame_acoes.pack(pady=15)

        customtkinter.CTkButton(frame_acoes, text="Salvar em .txt", command=marcar_item, height=35).pack(side=tk.LEFT, padx=10)
        customtkinter.CTkButton(frame_acoes, text="Copiar para Área de Transferência", command=copiar_itens, height=35, fg_color="#2FA572", hover_color="#106A43").pack(side=tk.LEFT, padx=10)

def main():
    root = customtkinter.CTk()
    app = MapeadorDiretoriosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()