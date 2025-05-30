import time

from gemini import gemini

def medir_tempo(func):
    inicio = time.time()
    func()
    fim = time.time()
    duracao = fim - inicio
    print(f"{func.__name__.upper()}: {duracao:.2f} s")

def main():
    medir_tempo(gemini)

if __name__ == "__main__":
    main()