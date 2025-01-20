# pip install pyautogui keyboard inputs

import pyautogui
import keyboard
import random
import time
import threading
import tkinter as tk

from tkinter import ttk
from inputs import devices, get_gamepad

class Ouvinte:
    def __init__(self, evento_parar):
        self.__lista_teclas = []
        self.__atalhos = {}
        self.__teclas_validas = []
        self.evento_parar = evento_parar

    def iniciar(self):
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

loop_ativo = False
clique_ativo = False
controle_ativo = False
teclas_selecionadas = []
botoes_controle_selecionados = []
tipo_clique_mouse = 'nenhum'
intervalo_teclado = (0.1, 0.5)
intervalo_controle = (0.1, 0.5)
threads_ativas = []
evento_parar = threading.Event()
eixos_controle = {}

mapa_botoes_controle = {
    'BTN_SOUTH': 'a',
    'BTN_EAST': 'b',
    'BTN_WEST': 'x',
    'BTN_NORTH': 'y',
    'BTN_TL': 'lb',
    'BTN_TR': 'rb',
    'ABS_Z': 'lt',
    'ABS_RZ':'rt'
}

def pressionar_tecla_aleatoriamente():
    global loop_ativo, intervalo_teclado
    while loop_ativo:
        if teclas_selecionadas:
            pyautogui.press(random.choice(teclas_selecionadas))
            time.sleep(random.uniform(*intervalo_teclado))

def clicar_mouse():
    global clique_ativo, tipo_clique_mouse
    while clique_ativo:
        if tipo_clique_mouse == 'esquerdo':
            pyautogui.click(button='left')
        elif tipo_clique_mouse == 'direito':
            pyautogui.click(button='right')
        time.sleep(0.1)

def pressionar_controle():
    global controle_ativo, intervalo_controle, botoes_controle_selecionados, eixos_controle
    while controle_ativo:
        if botoes_controle_selecionados:
            for event in get_gamepad():
              if event.ev_type == 'Key' and event.code in botoes_controle_selecionados and event.state == 1:
                tecla_correspondente = mapa_botoes_controle.get(event.code)
                if tecla_correspondente:
                    pyautogui.press(tecla_correspondente)
              elif event.ev_type == 'Absolute':
                    if event.code in mapa_botoes_controle:
                        eixos_controle[event.code] = event.state
                        if event.state > 20000:
                          tecla_correspondente = mapa_botoes_controle.get(event.code)
                          if tecla_correspondente:
                            pyautogui.press(tecla_correspondente)
            time.sleep(random.uniform(*intervalo_controle))
        else:
          time.sleep(0.1)

def alternar_loop():
    global loop_ativo, clique_ativo, controle_ativo, threads_ativas
    loop_ativo = not loop_ativo
    clique_ativo = loop_ativo
    controle_ativo = loop_ativo
    if loop_ativo:
        funcoes = [pressionar_tecla_aleatoriamente, clicar_mouse, pressionar_controle]
        for funcao in funcoes:
            thread = threading.Thread(target=funcao)
            threads_ativas.append(thread)
            thread.start()
    else:
        for thread in threads_ativas:
            thread.join()
        threads_ativas.clear()

def atualizar_teclas_selecionadas():
    global teclas_selecionadas
    teclas_selecionadas = [tecla for tecla, var in variaveis_teclas.items() if var.get()]

def atualizar_botoes_controle_selecionados():
    global botoes_controle_selecionados
    botoes_controle_selecionados = [botao for botao, var in variaveis_botoes_controle.items() if var.get()]

def atualizar_tipo_clique_mouse():
    global tipo_clique_mouse
    tipo_clique_mouse = variavel_mouse.get()

def fechar_app():
    global loop_ativo, clique_ativo, controle_ativo, evento_parar
    loop_ativo = False
    clique_ativo = False
    controle_ativo = False
    evento_parar.set()
    for thread in threads_ativas:
        thread.join()
    root.destroy()

def ao_fechar():
    fechar_app()

def main():
    global evento_parar, ouvinte, root, variaveis_teclas, variavel_mouse, variaveis_botoes_controle
    global intervalo_teclado_min, intervalo_teclado_max, intervalo_controle_min, intervalo_controle_max
    evento_parar = threading.Event()
    ouvinte = Ouvinte(evento_parar)
    ouvinte.adicionar_atalho('f4', alternar_loop)
    threading.Thread(target=ouvinte.iniciar).start()

    root = tk.Tk()
    root.title("Auto Clicker v1.0")
    root.geometry("540x405")
    root.protocol("WM_DELETE_WINDOW", ao_fechar)

    frame_principal = ttk.Frame(root)
    frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

    frame_teclas = ttk.LabelFrame(frame_principal, text="Teclas", labelanchor='n')
    frame_teclas.grid(row=0, column=0, padx=10, pady=10, sticky="n")
    variaveis_teclas = {}
    teclas = ['num1', 'num2', 'num3', 'num4', 'space']
    for tecla in teclas:
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame_teclas, text=tecla, variable=var, command=atualizar_teclas_selecionadas)
        chk.pack(anchor='w')
        variaveis_teclas[tecla] = var

    label_intervalo_teclado = ttk.Label(frame_teclas, text="Intervalo Teclado (s):")
    label_intervalo_teclado.pack(anchor='center', pady=5)
    frame_intervalo_teclado = ttk.Frame(frame_teclas)
    frame_intervalo_teclado.pack(anchor='center', pady=5)
    ttk.Label(frame_intervalo_teclado, text="Min:").pack(side='left')
    entry_intervalo_teclado_min = ttk.Entry(frame_intervalo_teclado, width=5)
    entry_intervalo_teclado_min.insert(0, f"{intervalo_teclado[0]}")
    entry_intervalo_teclado_min.pack(side='left', padx=5)
    ttk.Label(frame_intervalo_teclado, text="Max:").pack(side='left')
    entry_intervalo_teclado_max = ttk.Entry(frame_intervalo_teclado, width=5)
    entry_intervalo_teclado_max.insert(0, f"{intervalo_teclado[1]}")
    entry_intervalo_teclado_max.pack(side='left', padx=5)

    frame_mouse = ttk.LabelFrame(frame_principal, text="Mouse", labelanchor='n')
    frame_mouse.grid(row=0, column=1, padx=10, pady=10, sticky="n")
    variavel_mouse = tk.StringVar(value='nenhum')
    opcoes_mouse = [('Nenhum', 'nenhum'), ('Clique Esquerdo', 'esquerdo'), ('Clique Direito', 'direito')]
    for texto, valor in opcoes_mouse:
        rdo = ttk.Radiobutton(frame_mouse, text=texto, variable=variavel_mouse, value=valor,
                              command=atualizar_tipo_clique_mouse)
        rdo.pack(anchor='w')

    label_intervalo_mouse = ttk.Label(frame_mouse, text="Intervalo Movimento (s):")
    label_intervalo_mouse.pack(anchor='center', pady=5)
    frame_intervalo_mouse = ttk.Frame(frame_mouse)
    frame_intervalo_mouse.pack(anchor='center', pady=5)
    ttk.Label(frame_intervalo_mouse, text="Min:").pack(side='left')
    entry_intervalo_mouse_min = ttk.Entry(frame_intervalo_mouse, width=5)
    entry_intervalo_mouse_min.insert(0, "0.1")
    entry_intervalo_mouse_min.pack(side='left', padx=5)
    ttk.Label(frame_intervalo_mouse, text="Max:").pack(side='left')
    entry_intervalo_mouse_max = ttk.Entry(frame_intervalo_mouse, width=5)
    entry_intervalo_mouse_max.insert(0, "0.5")
    entry_intervalo_mouse_max.pack(side='left', padx=5)

    frame_controle = ttk.LabelFrame(frame_principal, text="Controle", labelanchor='n')
    frame_controle.grid(row=0, column=2, padx=10, pady=10, sticky="n")
    variaveis_botoes_controle = {}
    botoes_controle = {
        'A': 'BTN_SOUTH',
        'B': 'BTN_EAST',
        'X': 'BTN_WEST',
        'Y': 'BTN_NORTH',
        'LB': 'BTN_TL',
        'RB': 'BTN_TR',
        'LT': 'ABS_Z',
        'RT': 'ABS_RZ'
    }
    for texto, valor in botoes_controle.items():
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame_controle, text=texto, variable=var, command=atualizar_botoes_controle_selecionados)
        chk.pack(anchor='w')
        variaveis_botoes_controle[valor] = var

    label_intervalo_controle = ttk.Label(frame_controle, text="Intervalo Controle (s):")
    label_intervalo_controle.pack(anchor='center', pady=5)
    frame_intervalo_controle = ttk.Frame(frame_controle)
    frame_intervalo_controle.pack(anchor='center', pady=5)
    ttk.Label(frame_intervalo_controle, text="Min:").pack(side='left')
    entry_intervalo_controle_min = ttk.Entry(frame_intervalo_controle, width=5)
    entry_intervalo_controle_min.insert(0, "0.1")
    entry_intervalo_controle_min.pack(side='left', padx=5)
    ttk.Label(frame_intervalo_controle, text="Max:").pack(side='left')
    entry_intervalo_controle_max = ttk.Entry(frame_intervalo_controle, width=5)
    entry_intervalo_controle_max.insert(0, "0.5")
    entry_intervalo_controle_max.pack(side='left', padx=5)

    def atualizar_intervalos():
      global intervalo_teclado, intervalo_controle
      try:
          intervalo_teclado = (float(entry_intervalo_teclado_min.get()), float(entry_intervalo_teclado_max.get()))
          intervalo_controle = (float(entry_intervalo_controle_min.get()), float(entry_intervalo_controle_max.get()))
      except ValueError:
          entry_intervalo_teclado_min.delete(0, tk.END)
          entry_intervalo_teclado_min.insert(0, f"{intervalo_teclado[0]}")
          entry_intervalo_teclado_max.delete(0, tk.END)
          entry_intervalo_teclado_max.insert(0, f"{intervalo_teclado[1]}")
          entry_intervalo_controle_min.delete(0, tk.END)
          entry_intervalo_controle_min.insert(0, f"{intervalo_controle[0]}")
          entry_intervalo_controle_max.delete(0, tk.END)
          entry_intervalo_controle_max.insert(0, f"{intervalo_controle[1]}")

    botao_atualizar = ttk.Button(frame_principal, text="Atualizar Intervalos", command=atualizar_intervalos)
    botao_atualizar.grid(row=2, column=0, columnspan=3, pady=10)

    ttk.Button(frame_principal, text="Encerrar Aplicativo", command=fechar_app).grid(row=3, column=0,
                                                                                     columnspan=3,
                                                                                     pady=10)
    ttk.Label(root, text="Pressione F4 para iniciar ou parar o programa.").pack(pady=5)
    atualizar_intervalos()
    root.mainloop()

if __name__ == "__main__":
    main()