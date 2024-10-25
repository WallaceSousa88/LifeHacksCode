# pip install pyautogui keyboard

import pyautogui
import keyboard
import random
import time
import threading
import tkinter as tk

from tkinter import ttk

class Listener:
    def __init__(self):
        self.__listKey = []
        self.__hotkey = {}
        self.__validKey = []

    def start(self):
        while True:
            key = keyboard.read_event()
            if key.name in self.__validKey and key.event_type == 'down':
                if key.name not in self.__listKey:
                    self.__listKey.append(key.name)
                _hotkey = '+'.join(self.__listKey)
                if _hotkey in self.__hotkey:
                    func, args = self.__hotkey[_hotkey]
                    func(*args)
                else:
                    continue
            else:
                self.__listKey.clear()
                continue

    def addHotKey(self, hotkey, callback, *args):
        self.__hotkey[hotkey] = callback, args
        for _hotkey in hotkey.split('+'):
            self.__validKey.append(_hotkey)

loop_active = False
click_active = False
selected_keys = []
mouse_click_type = 'none'
keyboard_interval_range = (0.1, 0.3)

def press_key_randomly():
    while loop_active:
        if selected_keys:
            key_to_press = random.choice(selected_keys)
            pyautogui.press(key_to_press)
            time_interval = random.uniform(*keyboard_interval_range)
            time.sleep(time_interval)

def click_mouse():
    while click_active:
        if mouse_click_type == 'left':
            pyautogui.click(button='left')
        elif mouse_click_type == 'right':
            pyautogui.click(button='right')
        time.sleep(0.1)

def toggle_loop():
    global loop_active, click_active
    loop_active = not loop_active
    click_active = loop_active
    if loop_active:
        print("Loop ativado.")
        threading.Thread(target=press_key_randomly).start()
        threading.Thread(target=click_mouse).start()
    else:
        print("Loop desativado.")

def update_selected_keys():
    global selected_keys
    selected_keys = [key for key, var in key_vars.items() if var.get()]

def update_mouse_click_type():
    global mouse_click_type
    mouse_click_type = mouse_var.get()

def close_app():
    global loop_active, click_active
    loop_active = False
    click_active = False
    root.destroy()

def main():
    lis = Listener()
    lis.addHotKey('f4', toggle_loop)
    threading.Thread(target=lis.start).start()

    global root
    root = tk.Tk()
    root.title("Configurações do Loop")
    root.geometry("260x260")

    main_frame = ttk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill="both", expand=True)

    frame_keys = ttk.LabelFrame(main_frame, text="Teclas", labelanchor='n')
    frame_keys.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    global key_vars
    key_vars = {}
    keys = ['num1', 'num2', 'num3', 'num4', 'space']
    for key in keys:
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame_keys, text=key, variable=var, command=update_selected_keys)
        chk.pack(anchor='w')
        key_vars[key] = var

    frame_mouse = ttk.LabelFrame(main_frame, text="Mouse", labelanchor='n')
    frame_mouse.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    global mouse_var
    mouse_var = tk.StringVar(value='none')
    options = [('Nenhum', 'none'), ('Clique Esquerdo', 'left'), ('Clique Direito', 'right')]
    for text, value in options:
        rdo = ttk.Radiobutton(frame_mouse, text=text, variable=mouse_var, value=value, command=update_mouse_click_type)
        rdo.pack(anchor='w')

    ttk.Button(main_frame, text="Encerrar Aplicativo", command=close_app).grid(row=1, column=0, columnspan=2, pady=10)

    ttk.Label(root, text="Pressione F4 para iniciar ou parar o programa.").pack(pady=5)

    root.mainloop()

print("Pressione F4 para iniciar ou parar o programa.")
main()
