import customtkinter as ctk
import keyboard
import pyautogui
import random
import threading
import json
import os
import logging
import time

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
        self.teclas_config = [] # list of dicts: {"tecla": "a", "min": 0.1, "max": 0.5}
        self.tipo_clique_mouse = 'nenhum'
        self.intervalo_mouse = (0.1, 0.5)
        self.humanizar = False

    def _worker_tecla_individual(self, config):
        tecla = config.get("tecla")
        t_min = float(config.get("min", 0.1))
        t_max = float(config.get("max", 0.5))
        logging.info(f"Thread iniciada para tecla '{tecla}' ({t_min}s - {t_max}s).")
        try:
            while not self.stop_event.is_set():
                if self.humanizar:
                    pyautogui.keyDown(tecla)
                    time.sleep(random.uniform(0.05, 0.12))
                    pyautogui.keyUp(tecla)
                else:
                    pyautogui.press(tecla)
                    
                if self.stop_event.wait(random.uniform(t_min, t_max)):
                    break
        except Exception as e:
            logging.error(f"Erro na thread da tecla '{tecla}': {e}")

    def _worker_mouse(self):
        logging.info("Thread de Mouse iniciada.")
        try:
            while not self.stop_event.is_set():
                if self.tipo_clique_mouse != 'nenhum':
                    botao = 'left' if self.tipo_clique_mouse == 'esquerdo' else 'right'
                    
                    if self.humanizar:
                        pyautogui.mouseDown(button=botao)
                        time.sleep(random.uniform(0.05, 0.12))
                        pyautogui.mouseUp(button=botao)
                    else:
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
        for config in self.teclas_config:
            threading.Thread(target=self._worker_tecla_individual, args=(config,), daemon=True).start()
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
        self.geometry("600x550")
        self.lista_teclas = []
        self.grid_columnconfigure((0, 1), weight=1)
        self._criar_interface()
        self.carregar_config()
        keyboard.add_hotkey(ATALHO_GLOBAL, self.alternar_estado)

    def _criar_interface(self):
        # Frame Teclado
        self.frame_tec = ctk.CTkFrame(self)
        self.frame_tec.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.frame_tec, text="Teclado (Teclas Customizadas)", font=("Roboto", 14, "bold")).pack(pady=5)

        form_frame = ctk.CTkFrame(self.frame_tec, fg_color="transparent")
        form_frame.pack(fill="x", padx=10, pady=5)
        
        self.entry_nova_tecla = ctk.CTkEntry(form_frame, width=70, placeholder_text="Tecla")
        self.entry_nova_tecla.grid(row=0, column=0, padx=(0, 5), pady=2)
        
        self.entry_tec_min = ctk.CTkEntry(form_frame, width=50, placeholder_text="Mín(s)")
        self.entry_tec_min.grid(row=0, column=1, padx=(0, 5), pady=2)
        
        self.entry_tec_max = ctk.CTkEntry(form_frame, width=50, placeholder_text="Máx(s)")
        self.entry_tec_max.grid(row=0, column=2, padx=(0, 5), pady=2)
        
        btn_add = ctk.CTkButton(form_frame, text="+", width=30, command=self.adicionar_tecla)
        btn_add.grid(row=0, column=3, padx=0, pady=2)

        self.scroll_teclas = ctk.CTkScrollableFrame(self.frame_tec, height=200)
        self.scroll_teclas.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Frame Mouse
        self.frame_mou = ctk.CTkFrame(self)
        self.frame_mou.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.frame_mou, text="Mouse", font=("Roboto", 16, "bold")).pack(pady=5)

        self.mouse_var = ctk.StringVar(value="nenhum")
        for txt, val in [("Nenhum", "nenhum"), ("Esquerdo", "esquerdo"), ("Direito", "direito")]:
            ctk.CTkRadioButton(self.frame_mou, text=txt, variable=self.mouse_var, value=val).pack(pady=2, anchor="w", padx=20)

        ctk.CTkLabel(self.frame_mou, text="Intervalo (min/max):").pack(pady=(10, 0))
        interval_frame = ctk.CTkFrame(self.frame_mou, fg_color="transparent")
        interval_frame.pack(pady=5)
        self.mou_min = ctk.CTkEntry(interval_frame, width=60); self.mou_min.pack(side="left", padx=(0, 5))
        self.mou_max = ctk.CTkEntry(interval_frame, width=60); self.mou_max.pack(side="left")

        # Humanizar
        self.chk_humanizar_var = ctk.BooleanVar(value=False)
        self.chk_humanizar = ctk.CTkCheckBox(self, text="Humanizar Ações (Delay aleatório ao pressionar)", variable=self.chk_humanizar_var)
        self.chk_humanizar.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self, text="Salvar Configurações", fg_color="gray", command=self.salvar_config)
        self.btn_salvar.grid(row=2, column=0, columnspan=2, pady=10)

        # Status
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.canvas_status = ctk.CTkCanvas(self.status_frame, width=20, height=20, highlightthickness=0, bg="#2b2b2b")
        self.canvas_status.pack(side="left", padx=10)
        self.luz = self.canvas_status.create_oval(2, 2, 18, 18, fill="red")

        self.lbl_status = ctk.CTkLabel(self.status_frame, text=f"Status: PARADO (Atalho: {ATALHO_GLOBAL.upper()})", font=("Roboto", 13))
        self.lbl_status.pack(side="left")

    def adicionar_tecla(self):
        tecla = self.entry_nova_tecla.get().strip()
        t_min = self.entry_tec_min.get().strip()
        t_max = self.entry_tec_max.get().strip()

        if not tecla:
            return

        try:
            t_min_f = float(t_min) if t_min else 0.1
            t_max_f = float(t_max) if t_max else 0.5
            
            self.lista_teclas.append({
                "tecla": tecla,
                "min": t_min_f,
                "max": t_max_f
            })
            
            self.entry_nova_tecla.delete(0, 'end')
            self.entry_tec_min.delete(0, 'end')
            self.entry_tec_max.delete(0, 'end')
            
            self.atualizar_lista_teclas_ui()
        except ValueError:
            self.lbl_status.configure(text="Erro: Tempos da tecla inválidos", text_color="red")

    def remover_tecla(self, index):
        if 0 <= index < len(self.lista_teclas):
            del self.lista_teclas[index]
            self.atualizar_lista_teclas_ui()

    def atualizar_lista_teclas_ui(self):
        for widget in self.scroll_teclas.winfo_children():
            widget.destroy()
        
        for i, config in enumerate(self.lista_teclas):
            row_frame = ctk.CTkFrame(self.scroll_teclas, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            texto = f"{config['tecla']} ({config['min']}s - {config['max']}s)"
            lbl = ctk.CTkLabel(row_frame, text=texto, width=150, anchor="w")
            lbl.pack(side="left", padx=5)
            
            btn_del = ctk.CTkButton(row_frame, text="X", width=30, fg_color="#ef4444", hover_color="#dc2626",
                                    command=lambda idx=i: self.remover_tecla(idx))
            btn_del.pack(side="right", padx=5)

    def sincronizar_dados(self):
        try:
            self.automation.teclas_config = list(self.lista_teclas)
            self.automation.tipo_clique_mouse = self.mouse_var.get()
            self.automation.intervalo_mouse = (float(self.mou_min.get()), float(self.mou_max.get()))
            self.automation.humanizar = self.chk_humanizar_var.get()
            return True
        except ValueError:
            self.lbl_status.configure(text="Erro: Valores Numéricos do Mouse Inválidos", text_color="red")
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
            "lista_teclas": self.lista_teclas,
            "mouse": self.mouse_var.get(),
            "m_min": self.mou_min.get(), 
            "m_max": self.mou_max.get(),
            "humanizar": self.chk_humanizar_var.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Configurações salvas via UI.")

    def carregar_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    d = json.load(f)
                    
                    teclas_antigas = d.get("teclas", [])
                    t_min_antigo = d.get("t_min", "0.1")
                    t_max_antigo = d.get("t_max", "0.5")
                    
                    if "lista_teclas" in d:
                        self.lista_teclas = d["lista_teclas"]
                    else:
                        self.lista_teclas = [{"tecla": t, "min": float(t_min_antigo), "max": float(t_max_antigo)} for t in teclas_antigas]
                    
                    self.atualizar_lista_teclas_ui()
                    
                    self.mouse_var.set(d.get("mouse", "nenhum"))
                    self.mou_min.insert(0, d.get("m_min", "0.1"))
                    self.mou_max.insert(0, d.get("m_max", "0.5"))
                    self.chk_humanizar_var.set(d.get("humanizar", False))
                self.sincronizar_dados()
            except Exception as e:
                logging.error(f"Erro ao carregar JSON: {e}")
        else:
            self.mou_min.insert(0, "0.1")
            self.mou_max.insert(0, "0.5")

if __name__ == "__main__":
    app = App()
    app.mainloop()
