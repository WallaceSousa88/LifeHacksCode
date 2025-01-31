import os
import csv

def parse_time(time_str):
    parts = time_str.split(':')
    if len(parts) == 2:
        hours, minutes = map(int, parts)
        return hours * 60 + minutes
    elif len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 60 + minutes + seconds / 60
    return 0

def format_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"

def compare_values(value1, value2):
    return abs(parse_time(value1) - parse_time(value2))

def analyze_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        lines = list(reader)

        total_compensar = None
        total_excedente = None
        total_faltante = None
        total_horas_periodo = None
        total_horas_trabalhadas = None

        for line in lines:
            if len(line) == 0:
                continue
            if line[0].startswith('Total de Hora Compensar:'):
                total_compensar = line[0].split(': ')[1]
            elif line[0].startswith('Total de Horas Extras:'):
                total_excedente = line[0].split(': ')[1]
            elif line[0].startswith('Total de Horas do Período:'):
                total_horas_periodo = line[0].split(': ')[1]
            elif line[0].startswith("Total 'EXCEDENTE':"):
                total_excedente_python = line[0].split(': ')[1]
            elif line[0].startswith("Total 'FALTANTE':"):
                total_faltante_python = line[0].split(': ')[1]
            elif line[0].startswith("Total 'HORAS TRABALHADAS':"):
                total_horas_trabalhadas_python = line[0].split(': ')[1]

        errors = []

        if total_compensar and total_faltante_python:
            diff = compare_values(total_compensar.lstrip('-'), total_faltante_python)
            if diff != 0:
                errors.append(f"Diferença em 'Total de Hora Compensar' no arquivo {file_path.replace('\\', '/')} : {diff} minutos ({format_time(diff)}).")

        if total_excedente and total_excedente_python:
            diff = compare_values(total_excedente, total_excedente_python)
            if diff != 0:
                errors.append(f"Diferença em 'Total de Horas Extras' no arquivo {file_path.replace('\\', '/')} : {diff} minutos ({format_time(diff)}).")

        if total_horas_periodo and total_horas_trabalhadas_python:
            diff = compare_values(total_horas_periodo, total_horas_trabalhadas_python)
            if diff != 0:
                errors.append(f"Diferença em 'Total de Horas do Período' no arquivo {file_path.replace('\\', '/')} : {diff} minutos ({format_time(diff)}).")

        return errors

def analyze_files_in_directory(directory):
    report_lines = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            errors = analyze_csv(file_path)
            if errors:
                report_lines.extend(errors)

    report_file_path = os.path.join(directory, 'RELATORIO.txt')
    with open(report_file_path, 'w', encoding='utf-8') as report_file:
        if report_lines:
            report_file.write('\n'.join(report_lines))
        else:
            report_file.write('Nenhum erro encontrado.')

def main(output_folder='../out'):
    analyze_files_in_directory(output_folder)

if __name__ == "__main__":
    output_folder = '../out'
    main(output_folder)