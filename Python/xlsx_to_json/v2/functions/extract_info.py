import csv
import os

def extract_info(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        lines = list(reader)

        periodo_de = lines[3][0].strip() if len(lines) > 3 else 'N/A'
        periodo_ate = lines[4][0].strip() if len(lines) > 4 else 'N/A'
        nome = lines[6][2].strip() if len(lines[6]) > 2 else 'N/A'

        extracted_data = f"PERÍODO DE: {periodo_de} ATÉ: {periodo_ate}\n"
        extracted_data += f"NOME: {nome}\n\n"

        for line in lines[9:]:
            if "Vistos / Aprovações" in line or "FUNCIONÁRIO" in line:
                continue
            extracted_data += ';'.join(line) + '\n'

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(extracted_data)

if __name__ == "__main__":
    input_folder = os.path.join(os.path.dirname(__file__), '..', 'out')
    output_folder = os.path.join(os.path.dirname(__file__), '..', 'out')

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            extract_info(input_path, output_path)