# Requisitos
# pip install pynput
# pip install keyboard

from pynput.mouse import Button as MouseButton, Controller
import time
import keyboard
import threading
from tkinter import *

mouse = Controller()
auto_clicker_ativo = False
thread_auto_clicker = None

def auto_clicker(botao, tempo_entre_cliques):
    global auto_clicker_ativo

    if botao == "l":
        botao_mouse = MouseButton.left
    elif botao == "r":
        botao_mouse = MouseButton.right
    else:
        print("Botão inválido.")
        return

    def on_f4_press(event):
        global auto_clicker_ativo
        if event.event_type == 'down':
            return
        auto_clicker_ativo = not auto_clicker_ativo
        if auto_clicker_ativo:
            print("Auto Clicker ativado.")
        else:
            print("Auto Clicker desativado.")

    keyboard.hook_key('f4', on_f4_press)

    while True:
        if auto_clicker_ativo:
            mouse.press(botao_mouse)
            mouse.release(botao_mouse)
            time.sleep(tempo_entre_cliques)
        else:
            time.sleep(0.1)

def iniciar_auto_clicker():
    global thread_auto_clicker
    botao = var.get()
    tempo_entre_cliques = float(entry.get())
    thread_auto_clicker = threading.Thread(target=auto_clicker, args=(botao, tempo_entre_cliques))
    thread_auto_clicker.start()

root = Tk()

var = StringVar()
R1 = Radiobutton(root, text="Botão esquerdo", variable=var, value='l')
R1.pack( anchor = W )

R2 = Radiobutton(root, text="Botão direito", variable=var, value='r')
R2.pack( anchor = W )

Label(root, text="Intervalo entre cliques (em segundos):").pack()
entry = Entry(root)
entry.pack()

Button(root, text="Aplicar", command=iniciar_auto_clicker).pack()

root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()
