# pip install keyboard pyautogui

import keyboard
import pyautogui
import random
import time
import threading
import tkinter as tk

from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor

TECLAS_VALIDAS = ['num1', 'num2', 'num3', 'num4', 'space']
INTERVALO_TECLADO_PADRAO = (0.1, 0.5)
INTERVALO_MOUSE_PADRAO = (0.1, 0.5)
OPCOES_MOUSE = [('Nenhum', 'nenhum'), ('Clique Esquerdo', 'esquerdo'), ('Clique Direito', 'direito')]
ATALHO_ATIVAR_DESATIVAR = 'f4'

class Automation:
    def __init__(self):
      self.loop_ativo = False
      self.clique_ativo = False
      self.teclas_selecionadas = []
      self.tipo_clique_mouse = 'nenhum'
      self.intervalo_teclado = INTERVALO_TECLADO_PADRAO
      self.intervalo_mouse = INTERVALO_MOUSE_PADRAO
      self.executor = ThreadPoolExecutor(max_workers=2)
      self.futures = []

    def _pressionar_tecla_aleatoriamente(self):
        while self.loop_ativo:
            if self.teclas_selecionadas:
                pyautogui.press(random.choice(self.teclas_selecionadas))
                time.sleep(random.uniform(*self.intervalo_teclado))

    def _clicar_mouse(self):
        while self.clique_ativo:
            if self.tipo_clique_mouse == 'esquerdo':
                pyautogui.click(button='left')
            elif self.tipo_clique_mouse == 'direito':
                pyautogui.click(button='right')
            time.sleep(0.1)

    def iniciar_automacao(self):
        self.futures = []
        if self.loop_ativo:
            funcoes = [self._pressionar_tecla_aleatoriamente, self._clicar_mouse]
            for funcao in funcoes:
                future = self.executor.submit(funcao)
                self.futures.append(future)

    def parar_automacao(self):
        self.loop_ativo = False
        self.clique_ativo = False
        for future in self.futures:
            future.cancel()

class Control:
    def __init__(self, automation):
      self.evento_parar = threading.Event()
      self.automation = automation
      self.__lista_teclas = []
      self.__atalhos = {}
      self.__teclas_validas = []
      self._ouvindo = False

    def _iniciar_ouvinte_teclado(self):
      while not self.evento_parar.is_set():
            tecla = keyboard.read_event()
            if tecla.name in self.__teclas_validas and tecla.event_type == 'down':
                self.__lista_teclas.append(tecla.name)
                atalho = '+'.join(self.__lista_teclas)
                if atalho in self.__atalhos:
                    func, args = self.__atalhos[atalho]
                    func(*args)
                    self.__lista_teclas.clear()
            else:
                self.__lista_teclas.clear()

    def adicionar_atalho(self, atalho, callback, *args):
        self.__atalhos[atalho] = callback, args
        for tecla in atalho.split('+'):
            self.__teclas_validas.append(tecla)

    def alternar_loop(self, atualizar_status_callback):
        self.automation.loop_ativo = not self.automation.loop_ativo
        self.automation.clique_ativo = self.automation.loop_ativo
        if self.automation.loop_ativo:
            self.automation.iniciar_automacao()
        else:
            self.automation.parar_automacao()
        atualizar_status_callback()

    def iniciar_ouvinte(self):
      if not self._ouvindo:
        threading.Thread(target=self._iniciar_ouvinte_teclado).start()
        self._ouvindo = True

    def parar(self):
      self.evento_parar.set()

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker v1.0")
        self.root.geometry("500x410")
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)
        self.automation = Automation()
        self.control = Control(self.automation)
        self.control.adicionar_atalho(ATALHO_ATIVAR_DESATIVAR, self.control.alternar_loop, self.atualizar_status_label)
        self.control.iniciar_ouvinte()
        self._inicializar_layout()
        self.status_label = ttk.Label(root, text="Status: Desativado")
        self.status_label.pack(pady=5)
        ttk.Label(root, text=f"Pressione {ATALHO_ATIVAR_DESATIVAR} para iniciar ou parar o programa.").pack(pady=5)
        self._centralizar_janela()

    def _centralizar_janela(self):
      screen_width = self.root.winfo_screenwidth()
      screen_height = self.root.winfo_screenheight()
      x = (screen_width - 480) // 2
      y = (screen_height - 450) // 2
      self.root.geometry(f"500x410+{x}+{y}")

    def _inicializar_layout(self):
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(padx=10, pady=10, fill="both", expand=True)
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)

        self._criar_frame_teclas(frame_principal)
        self._criar_frame_mouse(frame_principal)

        ttk.Button(frame_principal, text="Atualizar Intervalos", command=self.atualizar_intervalos).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(frame_principal, text="Encerrar Aplicativo", command=self.fechar_app).grid(row=3, column=0, columnspan=2,pady=10)

    def _criar_frame_teclas(self, frame_principal):
        frame_teclas = ttk.LabelFrame(frame_principal, text="Teclas", labelanchor='n')
        frame_teclas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.variaveis_teclas = {}
        for tecla in TECLAS_VALIDAS:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame_teclas, text=tecla, variable=var, command=self.atualizar_teclas_selecionadas)
            chk.pack(anchor='w')
            self.variaveis_teclas[tecla] = var

        label_intervalo_teclado = ttk.Label(frame_teclas, text="Intervalo Teclado (s):")
        label_intervalo_teclado.pack(anchor='center', pady=5)
        frame_intervalo_teclado = ttk.Frame(frame_teclas)
        frame_intervalo_teclado.pack(anchor='center', pady=5)
        ttk.Label(frame_intervalo_teclado, text="Min:").pack(side='left')
        self.spin_intervalo_teclado_min = ttk.Spinbox(frame_intervalo_teclado, from_=0.01, to=10.0, width=5, increment=0.1)
        self.spin_intervalo_teclado_min.insert(0, f"{self.automation.intervalo_teclado[0]}")
        self.spin_intervalo_teclado_min.pack(side='left', padx=5)
        ttk.Label(frame_intervalo_teclado, text="Max:").pack(side='left')
        self.spin_intervalo_teclado_max = ttk.Spinbox(frame_intervalo_teclado, from_=0.01, to=10.0, width=5, increment=0.1)
        self.spin_intervalo_teclado_max.insert(0, f"{self.automation.intervalo_teclado[1]}")
        self.spin_intervalo_teclado_max.pack(side='left', padx=5)

    def _criar_frame_mouse(self, frame_principal):
      frame_mouse = ttk.LabelFrame(frame_principal, text="Mouse", labelanchor='n')
      frame_mouse.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
      self.variavel_mouse = tk.StringVar(value='nenhum')
      for texto, valor in OPCOES_MOUSE:
            rdo = ttk.Radiobutton(frame_mouse, text=texto, variable=self.variavel_mouse, value=valor,
                                  command=self.atualizar_tipo_clique_mouse)
            rdo.pack(anchor='w')

      label_intervalo_mouse = ttk.Label(frame_mouse, text="Intervalo Movimento (s):")
      label_intervalo_mouse.pack(anchor='center', pady=5)
      frame_intervalo_mouse = ttk.Frame(frame_mouse)
      frame_intervalo_mouse.pack(anchor='center', pady=5)
      ttk.Label(frame_intervalo_mouse, text="Min:").pack(side='left')
      self.spin_intervalo_mouse_min = ttk.Spinbox(frame_intervalo_mouse, from_=0.01, to=10.0, width=5, increment=0.1)
      self.spin_intervalo_mouse_min.insert(0, f"{self.automation.intervalo_mouse[0]}")
      self.spin_intervalo_mouse_min.pack(side='left', padx=5)
      ttk.Label(frame_intervalo_mouse, text="Max:").pack(side='left')
      self.spin_intervalo_mouse_max = ttk.Spinbox(frame_intervalo_mouse, from_=0.01, to=10.0, width=5, increment=0.1)
      self.spin_intervalo_mouse_max.insert(0, f"{self.automation.intervalo_mouse[1]}")
      self.spin_intervalo_mouse_max.pack(side='left', padx=5)

    def atualizar_teclas_selecionadas(self):
        self.automation.teclas_selecionadas = [tecla for tecla, var in self.variaveis_teclas.items() if var.get()]

    def atualizar_tipo_clique_mouse(self):
      self.automation.tipo_clique_mouse = self.variavel_mouse.get()

    def atualizar_intervalos(self):
        try:
            self.automation.intervalo_teclado = (float(self.spin_intervalo_teclado_min.get()), float(self.spin_intervalo_teclado_max.get()))
            self.automation.intervalo_mouse = (float(self.spin_intervalo_mouse_min.get()), float(self.spin_intervalo_mouse_max.get()))
        except ValueError:
            self.spin_intervalo_teclado_min.delete(0, tk.END)
            self.spin_intervalo_teclado_min.insert(0, f"{self.automation.intervalo_teclado[0]}")
            self.spin_intervalo_teclado_max.delete(0, tk.END)
            self.spin_intervalo_teclado_max.insert(0, f"{self.automation.intervalo_teclado[1]}")
            self.spin_intervalo_mouse_min.delete(0, tk.END)
            self.spin_intervalo_mouse_min.insert(0, f"{self.automation.intervalo_mouse[0]}")
            self.spin_intervalo_mouse_max.delete(0, tk.END)
            self.spin_intervalo_mouse_max.insert(0, f"{self.automation.intervalo_mouse[1]}")

    def atualizar_status_label(self):
        if self.automation.loop_ativo:
            self.status_label.config(text="Status: Ativado")
        else:
            self.status_label.config(text="Status: Desativado")

    def fechar_app(self):
        self.control.parar()
        self.root.destroy()

    def ao_fechar(self):
        self.fechar_app()

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()