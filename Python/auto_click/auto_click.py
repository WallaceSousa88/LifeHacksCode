# Requisitos
# pip install pynput
# pip install keyboard

from pynput.mouse import Button, Controller
import time
import keyboard

mouse = Controller()
auto_clicker_ativo = False

def auto_clicker():
    global auto_clicker_ativo
    botao = input("Qual botão do mouse? (L / R): ").lower()
    tempo_entre_cliques = float(input("Intervalo entre cliques (em segundos): "))

    if botao == "l":
        botao_mouse = Button.left
    elif botao == "r":
        botao_mouse = Button.right
    else:
        print("Botão inválido.")
        return

    print(f"Auto Clicker pronto para ser ativado com a tecla 'F4'.")

    while True:
        if keyboard.is_pressed('f4'):
            auto_clicker_ativo = not auto_clicker_ativo
            if auto_clicker_ativo:
                print("Auto Clicker ativado.")
            else:
                print("Auto Clicker desativado.")

        if auto_clicker_ativo:
            mouse.press(botao_mouse)
            mouse.release(botao_mouse)
            time.sleep(tempo_entre_cliques)
        time.sleep(0.1)

auto_clicker()
