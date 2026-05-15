# pip install customtkinter keyboard pyautogui

import customtkinter as ctk
import keyboard
import pyautogui
import random
import threading
import json
import os
import logging

CONFIG_FILE = "config.json"
LOG_FILE = "automacao.log"
ATALHO_GLOBAL = 'f4'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Automation:
    def __init__(self, ui_callback):
        pyautogui.FAILSAFE = True
        self.stop_event = threading.Event()
        self.loop_ativo = False
        self.ui_callback = ui_callback
        self.teclas_selecionadas = []
        self.tipo_clique_mouse = 'nenhum'
        self.intervalo_teclado = (0.1, 0.5)
        self.intervalo_mouse = (0.1, 0.5)

    def _worker_teclado(self):
        logging.info("Thread de Teclado iniciada.")
        try:
            while not self.stop_event.is_set():
                if self.teclas_selecionadas:
                    tecla = random.choice(self.teclas_selecionadas)
                    pyautogui.press(tecla)
                    if self.stop_event.wait(random.uniform(*self.intervalo_teclado)):
                        break
                else:
                    self.stop_event.wait(0.2)
        except Exception as e:
            logging.error(f"Erro na thread de teclado: {e}")

    def _worker_mouse(self):
        logging.info("Thread de Mouse iniciada.")
        try:
            while not self.stop_event.is_set():
                if self.tipo_clique_mouse != 'nenhum':
                    botao = 'left' if self.tipo_clique_mouse == 'esquerdo' else 'right'
                    pyautogui.click(button=botao)
                    if self.stop_event.wait(random.uniform(*self.intervalo_mouse)):
                        break
                else:
                    self.stop_event.wait(0.2)
        except pyautogui.FailSafeException:
            logging.warning("FAILSAFE disparado pelo usuário!")
            self.ui_callback("emergencia", "FAILSAFE ATIVADO")
        except Exception as e:
            logging.error(f"Erro na thread de mouse: {e}")

    def iniciar(self):
        self.stop_event.clear()
        self.loop_ativo = True
        threading.Thread(target=self._worker_teclado, daemon=True).start()
        threading.Thread(target=self._worker_mouse, daemon=True).start()

    def parar(self):
        self.loop_ativo = False
        self.stop_event.set()
        logging.info("Automação solicitou parada.")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.automation = Automation(self.callback_emergencia)
        self.title("AutoPro Clicker v3.0")
        self.geometry("520x550")
        self.grid_columnconfigure((0, 1), weight=1)
        self._criar_interface()
        self.carregar_config()
        keyboard.add_hotkey(ATALHO_GLOBAL, self.alternar_estado)

    def _criar_interface(self):
        self.frame_tec = ctk.CTkFrame(self)
        self.frame_tec.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.frame_tec, text="Teclado", font=("Roboto", 16, "bold")).pack(pady=5)

        self.chk_vars = {}
        for tecla in ['num1', 'num2', 'num3', 'num4', 'space']:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(self.frame_tec, text=tecla.upper(), variable=var).pack(pady=2, anchor="w", padx=20)
            self.chk_vars[tecla] = var

        ctk.CTkLabel(self.frame_tec, text="Intervalo (min/max):").pack(pady=(10, 0))
        self.tec_min = ctk.CTkEntry(self.frame_tec, width=60); self.tec_min.pack(side="left", padx=(20, 5), pady=5)
        self.tec_max = ctk.CTkEntry(self.frame_tec, width=60); self.tec_max.pack(side="left", padx=5, pady=5)

        self.frame_mou = ctk.CTkFrame(self)
        self.frame_mou.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.frame_mou, text="Mouse", font=("Roboto", 16, "bold")).pack(pady=5)

        self.mouse_var = ctk.StringVar(value="nenhum")
        for txt, val in [("Nenhum", "nenhum"), ("Esquerdo", "esquerdo"), ("Direito", "direito")]:
            ctk.CTkRadioButton(self.frame_mou, text=txt, variable=self.mouse_var, value=val).pack(pady=2, anchor="w", padx=20)

        ctk.CTkLabel(self.frame_mou, text="Intervalo (min/max):").pack(pady=(10, 0))
        self.mou_min = ctk.CTkEntry(self.frame_mou, width=60); self.mou_min.pack(side="left", padx=(20, 5), pady=5)
        self.mou_max = ctk.CTkEntry(self.frame_mou, width=60); self.mou_max.pack(side="left", padx=5, pady=5)

        self.btn_salvar = ctk.CTkButton(self, text="Salvar Configurações", fg_color="gray", command=self.salvar_config)
        self.btn_salvar.grid(row=1, column=0, columnspan=2, pady=10)

        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.canvas_status = ctk.CTkCanvas(self.status_frame, width=20, height=20, highlightthickness=0, bg="#2b2b2b")
        self.canvas_status.pack(side="left", padx=10)
        self.luz = self.canvas_status.create_oval(2, 2, 18, 18, fill="red")

        self.lbl_status = ctk.CTkLabel(self.status_frame, text=f"Status: PARADO (Atalho: {ATALHO_GLOBAL.upper()})", font=("Roboto", 13))
        self.lbl_status.pack(side="left")

    def sincronizar_dados(self):
        try:
            self.automation.teclas_selecionadas = [t for t, v in self.chk_vars.items() if v.get()]
            self.automation.tipo_clique_mouse = self.mouse_var.get()
            self.automation.intervalo_teclado = (float(self.tec_min.get()), float(self.tec_max.get()))
            self.automation.intervalo_mouse = (float(self.mou_min.get()), float(self.mou_max.get()))
            return True
        except ValueError:
            self.lbl_status.configure(text="Erro: Valores Numéricos Inválidos", text_color="red")
            return False

    def alternar_estado(self):
        if self.automation.loop_ativo:
            self.automation.parar()
            self.lbl_status.configure(text=f"Status: PARADO", text_color="white")
            self.canvas_status.itemconfig(self.luz, fill="red")
        else:
            if self.sincronizar_dados():
                self.automation.iniciar()
                self.lbl_status.configure(text="Status: RODANDO", text_color="#4ade80")
                self.canvas_status.itemconfig(self.luz, fill="green")

    def callback_emergencia(self, tipo, msg):
        self.lbl_status.configure(text=f"STATUS: {msg}", text_color="orange")
        self.canvas_status.itemconfig(self.luz, fill="orange")
        self.automation.loop_ativo = False

    def salvar_config(self):
        data = {
            "teclas": [t for t, v in self.chk_vars.items() if v.get()],
            "mouse": self.mouse_var.get(),
            "t_min": self.tec_min.get(), "t_max": self.tec_max.get(),
            "m_min": self.mu_min.get() if hasattr(self, 'mou_min') else "0.1",
            "m_min": self.mou_min.get(), "m_max": self.mou_max.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Configurações salvas via UI.")

    def carregar_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    d = json.load(f)
                    for t, v in self.chk_vars.items(): v.set(t in d.get("teclas", []))
                    self.mouse_var.set(d.get("mouse", "nenhum"))
                    self.tec_min.insert(0, d.get("t_min", "0.1"))
                    self.tec_max.insert(0, d.get("t_max", "0.5"))
                    self.mou_min.insert(0, d.get("m_min", "0.1"))
                    self.mou_max.insert(0, d.get("m_max", "0.5"))
                self.sincronizar_dados()
            except Exception as e:
                logging.error(f"Erro ao carregar JSON: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
