import os
import tkinter as tk
from tkinter import filedialog, messagebox
from functions.extract_pdf import extract_pdf
from functions.format_csv_1 import extract_info
from functions.format_csv_2 import process_csv_files
from functions.calculate_hours import process_csv
from functions.report import analyze_files_in_directory
import pyperclip
from PIL import Image, ImageTk
from datetime import datetime

def browse_input_folder():
    input_folder = filedialog.askdirectory(title="Selecione a pasta 'in'")
    if input_folder:
        input_folder_entry.delete(0, tk.END)
        input_folder_entry.insert(0, input_folder.replace('\\', '/'))
        update_output_folder()

def update_output_folder():
    input_folder = input_folder_entry.get()
    if input_folder:
        output_folder = os.path.join(os.path.dirname(input_folder), 'out').replace('\\', '/')
        output_folder_entry.config(state=tk.NORMAL)
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, output_folder)
        output_folder_entry.config(state=tk.DISABLED)

def run_processing():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()

    if not input_folder:
        status_label.config(text="Selecione a pasta 'in' primeiro.")
        return

    try:
        log = []

        start_time = datetime.now().strftime("%H:%M:%S")
        log.append(f"{start_time} - Início do processamento")

        status_label.config(text="Extraindo PDFs...")
        start_time = datetime.now().strftime("%H:%M:%S")
        log.append(f"{start_time} - Extraindo PDFs...")
        extract_pdf(input_folder, output_folder)

        status_label.config(text="Formatando CSV (etapa 1)...")
        start_time = datetime.now().strftime("%H:%M:%S")
        log.append(f"{start_time} - Formatando CSV (etapa 1)...")
        extract_info(output_folder)

        status_label.config(text="Formatando CSV (etapa 2)...")
        start_time = datetime.now().strftime("%H:%M:%S")
        log.append(f"{start_time} - Formatando CSV (etapa 2)...")
        process_csv_files(output_folder)

        status_label.config(text="Calculando horas...")
        start_time = datetime.now().strftime("%H:%M:%S")
        log.append(f"{start_time} - Calculando horas...")
        process_csv(output_folder)

        status_label.config(text="Analisando arquivos...")
        start_time = datetime.now().strftime("%H:%M:%S")
        log.append(f"{start_time} - Analisando arquivos...")
        analyze_files_in_directory(output_folder)

        end_time = datetime.now().strftime("%H:%M:%S")
        log.append(f"{end_time} - Processamento concluído com sucesso!")

        formatted_log = "\n".join(log)

        log_text_widget.config(state=tk.NORMAL)
        log_text_widget.delete(1.0, tk.END)
        log_text_widget.insert(tk.END, formatted_log)
        log_text_widget.config(state=tk.DISABLED)

    except Exception as e:
        status_label.config(text=f"Erro durante o processamento: {e}")

def copy_path(entry_widget):
    path = entry_widget.get()
    if path:
        try:
            pyperclip.copy(path)
        except pyperclip.PyperclipException:
           messagebox.showerror("Erro", "Não foi possível copiar para a área de transferência. Por favor, tente novamente.")
    else:
         messagebox.showwarning("Atenção!", "Selecione a pasta primeiro.")

def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window = tk.Tk()
window.title("Processador de Arquivos")
window.geometry("500x400")

copy_icon_image = Image.open("copy_icon.png")
copy_icon_image = copy_icon_image.resize((20, 20), Image.LANCZOS)
copy_icon = ImageTk.PhotoImage(copy_icon_image)

button_margin_x = 5
button_margin_y = 0
button_size_percentage = 1

input_label = tk.Label(window, text="Pasta Entrada (.pdf):")
input_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
input_folder_entry = tk.Entry(window, width=60)
input_folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

label_height = input_label.winfo_reqheight()
button_size = int(label_height * button_size_percentage)

copy_input_button = tk.Button(window, image=copy_icon, command=lambda: copy_path(input_folder_entry), width=button_size, height=button_size,  borderwidth=0)
copy_input_button.grid(row=0, column=2, padx=(button_margin_x, 5), pady=button_margin_y, sticky='w')

output_label = tk.Label(window, text="Pasta Saida (.csv):")
output_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
output_folder_entry = tk.Entry(window, width=60, state=tk.DISABLED)
output_folder_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

label_height = output_label.winfo_reqheight()
button_size = int(label_height * button_size_percentage)

copy_output_button = tk.Button(window, image=copy_icon, command=lambda: copy_path(output_folder_entry), width=button_size, height=button_size, borderwidth=0)
copy_output_button.grid(row=1, column=2, padx=(button_margin_x, 5), pady=button_margin_y, sticky='w')

browse_button = tk.Button(window, text="1. Selecione a pasta para analisar.", command=browse_input_folder)
browse_button.grid(row=2, column=0, columnspan=3, pady=5)

process_button = tk.Button(window, text="2. Iniciar Processamento", command=run_processing)
process_button.grid(row=3, column=0, columnspan=3, pady=10)

status_label = tk.Label(window, text="")
status_label.grid(row=4, column=0, columnspan=3, pady=10)

log_text_widget = tk.Text(window, wrap=tk.WORD, padx=20, pady=20, state=tk.DISABLED, bg=window.cget("bg"), relief=tk.FLAT)
log_text_widget.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

window.columnconfigure(1, weight=1)
window.rowconfigure(5, weight=1)

window.after(100, lambda: center_window(window))
window.mainloop()