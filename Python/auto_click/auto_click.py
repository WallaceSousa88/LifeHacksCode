# Requisitos
# pip install pynput
# pip install keyboard

import pyautogui
import keyboard
import random
import time
import threading
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class Listener:
    def __init__(self):
        self.__listKey = []
        self.__hotkey = {}
        self.__validKey = []

    def start(self):
        while True:
            try:
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
            except Exception as e:
                logging.error("Erro ocorrido", exc_info=True)

    def addHotKey(self, hotkey, callback, *args):
        self.__hotkey[hotkey] = callback, args
        for _hotkey in hotkey.split('+'):
            self.__validKey.append(_hotkey)

loop_active = False

def press_key_randomly():
    keys = ['num1', 'num2', 'num3', 'num4']
    while loop_active:
        try:
            key_to_press = random.choice(keys)
            pyautogui.press(key_to_press)
            time_interval = random.uniform(0.1, 1)
            time.sleep(time_interval)
        except Exception as e:
            logging.error("Erro ocorrido", exc_info=True)

def toggle_loop():
    global loop_active
    loop_active = not loop_active
    if loop_active:
        print("Loop ativado.")
        threading.Thread(target=press_key_randomly).start()
    else:
        print("Loop desativado.")

def main():
    lis = Listener()
    lis.addHotKey('f4', toggle_loop)
    lis.start()

print("Pressione F4 para iniciar ou parar o programa.")
main()
