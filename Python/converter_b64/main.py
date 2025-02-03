import base64
import os
import shutil

def encode_file_to_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

def decode_base64_to_file(base64_string, output_path):
    with open(output_path, "wb") as file:
        file.write(base64.b64decode(base64_string))

def encode_files_in_folder(input_folder, output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            encoded_string = encode_file_to_base64(file_path)
            output_file_path = os.path.join(output_folder, filename + ".txt")
            with open(output_file_path, "w") as output_file:
                output_file.write(encoded_string)

def decode_files_in_folder(output_folder):
    for filename in os.listdir(output_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(output_folder, filename)
            with open(file_path, "r") as file:
                base64_string = file.read()
            original_filename = filename[:-4]
            original_file_path = os.path.join(output_folder, original_filename)
            decode_base64_to_file(base64_string, original_file_path)
            os.remove(file_path)

def main():
    print("Escolha uma opção:")
    print("1. Codificar arquivos para Base64")
    print("2. Decodificar arquivos de Base64 para o formato original")

    choice = input("Digite 1 ou 2: ")

    if choice == '1':
        input_folder = input("Digite o caminho da pasta de entrada: ")
        output_folder = "out"
        encode_files_in_folder(input_folder, output_folder)
        print(f"Arquivos codificados e salvos na pasta '{output_folder}'")
    elif choice == '2':
        output_folder = "out"
        decode_files_in_folder(output_folder)
        print(f"Arquivos decodificados e salvos na pasta '{output_folder}'")
    else:
        print("Opção inválida. Por favor, escolha 1 ou 2.")

if __name__ == "__main__":
    main()