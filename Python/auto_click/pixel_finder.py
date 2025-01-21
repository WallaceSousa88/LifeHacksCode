# pip install pygetwindow tk

import tkinter as tk
import pygetwindow as gw

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
WINDOW_TITLE = "Pixel Finder"

def create_window():
    root = tk.Tk()
    root.title(WINDOW_TITLE)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2

    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    return root

def get_window_titles():
    windows = gw.getWindowsWithTitle('')
    return [window.title for window in windows if window.title]

def create_listbox(root, window_titles):
    listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    for title in window_titles:
        listbox.insert(tk.END, title)
    listbox.pack(pady=20, expand=True, fill=tk.BOTH)
    return listbox

def get_selected_window_size(root, listbox):
    selected_title = listbox.get(tk.ACTIVE)
    if not selected_title:
        return

    windows = gw.getWindowsWithTitle('')
    selected_window = next((window for window in windows if window.title == selected_title), None)
    if not selected_window:
        print ("Janela não encontrada")
        return

    width, height = selected_window.width, selected_window.height
    print(f"Largura: {width}, Altura: {height}")
    root.destroy()

def create_button(root, listbox):
    button = tk.Button(root, text="Obter Tamanho da Janela",
                         command=lambda: get_selected_window_size(root, listbox))
    button.pack(pady=20)

def on_closing(root):
    root.destroy()

def get_window_size():
    root = create_window()
    window_titles = get_window_titles()
    listbox = create_listbox(root, window_titles)
    create_button(root, listbox)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

if __name__ == "__main__":
    get_window_size()