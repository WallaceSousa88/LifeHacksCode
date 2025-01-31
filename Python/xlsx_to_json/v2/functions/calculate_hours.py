import os
import csv
from datetime import datetime, timedelta

def time_to_timedelta(time_str):
    if not time_str:
        return timedelta()
    try:
        t = datetime.strptime(time_str, '%H:%M')
        return timedelta(hours=t.hour, minutes=t.minute)
    except ValueError:
        return timedelta()

def process_csv(output_folder):
    for filename in os.listdir(output_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(output_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            header = lines[:3]
            data = lines[3:-4]
            footer = lines[-4:]

            total_excedente = timedelta()
            total_faltante = timedelta()
            total_worked_hours = timedelta()
            weekend_entries = []
            excedente_errors = []
            faltante_errors = []

            for row in csv.reader(data, delimiter=';'):
                day, week_day, entrada_manha, saida_manha, entrada_tarde, saida_tarde, excedente, faltante, observacao = row

                total_excedente += time_to_timedelta(excedente)
                total_faltante += time_to_timedelta(faltante)

                worked_hours_manha = time_to_timedelta(saida_manha) - time_to_timedelta(entrada_manha)
                worked_hours_tarde = time_to_timedelta(saida_tarde) - time_to_timedelta(entrada_tarde)
                worked_hours_day = worked_hours_manha + worked_hours_tarde
                total_worked_hours += worked_hours_day

                if week_day.lower() in ['sáb', 'sab', 'dom']:
                    if entrada_manha or saida_manha or entrada_tarde or saida_tarde or excedente or faltante:
                        weekend_entries.append(day)

                if worked_hours_day > timedelta(hours=8):
                    expected_excedente = worked_hours_day - timedelta(hours=8)
                    if time_to_timedelta(excedente) != expected_excedente:
                        excedente_errors.append(day)

                if not observacao and week_day.lower() not in ['sáb', 'sab', 'dom'] and worked_hours_day < timedelta(hours=8):
                    expected_faltante = timedelta(hours=8) - worked_hours_day
                    if time_to_timedelta(faltante) != expected_faltante:
                        faltante_errors.append(day)

            analysis_header = "--- Analise Python ---\n\n"
            analysis_results = [
                f"Total 'EXCEDENTE': {str(total_excedente)[:-3]}\n",
                f"Total 'FALTANTE': {int(total_faltante.total_seconds() // 3600)}:{str(int((total_faltante.total_seconds() % 3600) // 60)).zfill(2)}\n",
                f"Total 'HORAS TRABALHADAS': {str(int(total_worked_hours.total_seconds() // 3600))}:{str(int((total_worked_hours.total_seconds() % 3600) // 60)).zfill(2)}\n"
            ]

            errors_header = "\n--- Erros ---\n"
            errors_results = []

            if weekend_entries:
                errors_results.append(f"Registros em fim de semana: {', '.join(weekend_entries)}\n")

            if excedente_errors:
                errors_results.append(f"Erros em EXCEDENTE nos dias: {', '.join(excedente_errors)}\n")

            if faltante_errors:
                errors_results.append(f"Erros em FALTANTE nos dias: {', '.join(faltante_errors)}\n")

            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(header + data + footer + ['\n'] + [analysis_header] + analysis_results + (errors_results and [errors_header] + errors_results))

def main():
    output_folder = '../out'
    process_csv(output_folder)
    print("Arquivos CSV processados com sucesso.")

if __name__ == "__main__":
    main()