import tkinter as tk

def get_window_size():
    root = tk.Tk()
    root.title("Ajuste o tamanho da janela e clique no botão")

    def show_size():
        width = root.winfo_width()
        height = root.winfo_height()
        print(f"Largura: {width}, Altura: {height}")
        root.destroy()
        input("Pressione Enter para sair...")

    button = tk.Button(root, text="Obter Tamanho da Janela", command=show_size)
    button.pack(pady=20)
    root.mainloop()

get_window_size()