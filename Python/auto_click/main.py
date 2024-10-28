# pip install pyautogui keyboard

import pyautogui
import keyboard
import random
import time
import threading
import tkinter as tk
import math

from tkinter import ttk

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
movimento_circular_ativo = False
teclas_selecionadas = []
tipo_clique_mouse = 'nenhum'
intervalo_teclado = (0.1, 0.5)
intervalo_movimento_circular = (0.1, 0.5)
threads_ativas = []
evento_parar = threading.Event()

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

largura_tela, altura_tela = pyautogui.size()
centro_x, centro_y = largura_tela // 2, altura_tela // 2

def mover_mouse_em_circulo():
    global movimento_circular_ativo, intervalo_movimento_circular
    while movimento_circular_ativo:
        angulo = random.uniform(0, 2 * 3.14159)
        variacao_raio = random.uniform(-5, 5)
        raio = 25 + variacao_raio
        novo_x = centro_x + int(raio * math.cos(angulo))
        novo_y = centro_y + int(raio * math.sin(angulo))
        pyautogui.moveTo(novo_x, novo_y, duration=random.uniform(0.1, 0.4))
        time.sleep(random.uniform(*intervalo_movimento_circular))

def alternar_loop():
    global loop_ativo, clique_ativo, movimento_circular_ativo, threads_ativas
    loop_ativo = not loop_ativo
    clique_ativo = loop_ativo
    movimento_circular_ativo = loop_ativo if variavel_movimento_circular.get() else False

    if loop_ativo:
        for funcao in [pressionar_tecla_aleatoriamente, clicar_mouse, mover_mouse_em_circulo]:
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

def atualizar_tipo_clique_mouse():
    global tipo_clique_mouse
    tipo_clique_mouse = variavel_mouse.get()

def atualizar_movimento_circular():
    global movimento_circular_ativo
    movimento_circular_ativo = variavel_movimento_circular.get()

def fechar_app():
    global loop_ativo, clique_ativo, movimento_circular_ativo, evento_parar
    loop_ativo = False
    clique_ativo = False
    movimento_circular_ativo = False
    evento_parar.set()
    for thread in threads_ativas:
        thread.join()
    root.destroy()

def ao_fechar():
    fechar_app()

def main():
    global evento_parar, ouvinte, root, variaveis_teclas, variavel_mouse
    global variavel_movimento_circular, intervalo_teclado, intervalo_movimento_circular
    evento_parar = threading.Event()
    ouvinte = Ouvinte(evento_parar)
    ouvinte.adicionar_atalho('f4', alternar_loop)
    threading.Thread(target=ouvinte.iniciar).start()

    root = tk.Tk()
    root.title("Configurações do Loop")
    root.geometry("340x325")
    root.protocol("WM_DELETE_WINDOW", ao_fechar)

    frame_principal = ttk.Frame(root)
    frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

    frame_teclas = ttk.LabelFrame(frame_principal, text="Teclas")
    frame_teclas.grid(row=0, column=0, padx=10, pady=10, sticky="n")
    variaveis_teclas = {}
    teclas = ['num1', 'num2', 'num3', 'num4', 'space']
    for tecla in teclas:
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame_teclas, text=tecla, variable=var, command=atualizar_teclas_selecionadas)
        chk.pack(anchor='w')
        variaveis_teclas[tecla] = var

    label_intervalo_teclado = ttk.Label(frame_teclas, text="Intervalo Teclado (s):")
    label_intervalo_teclado.pack(anchor='w')
    entry_intervalo_teclado = ttk.Entry(frame_teclas, width=10)
    entry_intervalo_teclado.insert(0, f"{intervalo_teclado[0]},{intervalo_teclado[1]}")
    entry_intervalo_teclado.pack(anchor='w')

    frame_mouse = ttk.LabelFrame(frame_principal, text="Mouse")
    frame_mouse.grid(row=0, column=1, padx=10, pady=10, sticky="n")
    variavel_mouse = tk.StringVar(value='nenhum')
    opcoes_mouse = [('Nenhum', 'nenhum'), ('Clique Esquerdo', 'esquerdo'), ('Clique Direito', 'direito')]
    for texto, valor in opcoes_mouse:
        rdo = ttk.Radiobutton(frame_mouse, text=texto, variable=variavel_mouse, value=valor,
                              command=atualizar_tipo_clique_mouse)
        rdo.pack(anchor='w')
    variavel_movimento_circular = tk.BooleanVar(value=False)
    chk_movimento_circular = ttk.Checkbutton(frame_mouse, text="Ativar Movimento Circular",
                                             variable=variavel_movimento_circular,
                                             command=atualizar_movimento_circular)
    chk_movimento_circular.pack(anchor='w')

    label_intervalo_mouse = ttk.Label(frame_mouse, text="Intervalo Movimento (s):")
    label_intervalo_mouse.pack(anchor='w')
    entry_intervalo_mouse = ttk.Entry(frame_mouse, width=10)
    entry_intervalo_mouse.insert(0, f"{intervalo_movimento_circular[0]},{intervalo_movimento_circular[1]}")
    entry_intervalo_mouse.pack(anchor='w')

    def atualizar_intervalos():
        global intervalo_teclado, intervalo_movimento_circular
        try:
            intervalo_teclado = tuple(float(x) for x in entry_intervalo_teclado.get().split(","))
        except ValueError:
            entry_intervalo_teclado.delete(0, tk.END)
            entry_intervalo_teclado.insert(0, f"{intervalo_teclado[0]},{intervalo_teclado[1]}")
        try:
            intervalo_movimento_circular = tuple(float(x) for x in entry_intervalo_mouse.get().split(","))
        except ValueError:
            entry_intervalo_mouse.delete(0, tk.END)
            entry_intervalo_mouse.insert(0, f"{intervalo_movimento_circular[0]},{intervalo_movimento_circular[1]}")

    botao_atualizar = ttk.Button(frame_principal, text="Atualizar Intervalos", command=atualizar_intervalos)
    botao_atualizar.grid(row=2, column=0, columnspan=2, pady=10)

    ttk.Button(frame_principal, text="Encerrar Aplicativo", command=fechar_app).grid(row=3, column=0,
                                                                                     columnspan=2,
                                                                                     pady=10)
    ttk.Label(root, text="Pressione F4 para iniciar ou parar o programa.").pack(pady=5)
    atualizar_intervalos()
    root.mainloop()

if __name__ == "__main__":
    main()
