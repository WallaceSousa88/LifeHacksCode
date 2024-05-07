import subprocess

def main():
    while True:
        print("Escolha uma opção:")
        print("1. Converter HTML para Excel")
        print("2. Mapear diretório")
        print("3. Sair")
        escolha = input("Digite o número da opção desejada: ")
        
        if escolha == '1':
            subprocess.run(["python", "./html_to_excel/html_to_excel.py"])
        elif escolha == '2':
            subprocess.run(["python", "./map_diretorio/map_diretorio.py"])
        elif escolha == '3':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
