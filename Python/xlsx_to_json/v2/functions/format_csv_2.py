import os

def modify_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    header = lines[:3]
    data_lines = lines[3:-6]
    footer = lines[-6:]

    footer_modified = [
        '\n',
        f'Total de Hora Compensar: {footer[2].split(";")[4]}\n',
        f'Total de Horas Extras: {footer[3].split(";")[4]}\n',
        f'Total de Horas do Período: {footer[5].split(";")[4]}\n'
    ]

    data_modified = ['DIA;SEMANA;ENTRADA MANHA;SAIDA MANHA;ENTRADA TARDE;SAIDA TARDE;EXCEDENTE;FALTANTE;OBSERVACAO\n']
    for line in data_lines:
        columns = line.split(';')
        if columns[0].isdigit():
            new_columns = [
                columns[0],
                columns[1],
                '' if columns[2] in ['00:00', '0:0', '0:00'] else columns[2],
                '' if columns[3] in ['00:00', '0:0', '0:00'] else columns[3],
                '' if columns[4] in ['00:00', '0:0', '0:00'] else columns[4],
                '' if columns[6] in ['00:00', '0:0', '0:00'] else columns[6],
                '' if columns[8] in ['00:00', '0:0', '0:00'] else columns[8],
                '' if columns[11] in ['00:00', '0:0', '0:00'] else columns[11],
                columns[12]
            ]
            data_modified.append(';'.join(new_columns) + '\n')

    new_content = header + data_modified + footer_modified

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_content)

def process_csv_files(output_folder):
    for filename in os.listdir(output_folder):
        if filename.endswith('.csv'):
            modify_csv(os.path.join(output_folder, filename))

if __name__ == "__main__":
    output_folder = '../out'
    process_csv_files(output_folder)
    print("Modificações aplicadas com sucesso aos arquivos CSV na pasta 'out'.")