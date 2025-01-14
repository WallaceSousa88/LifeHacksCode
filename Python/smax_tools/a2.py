import chardet
import csv
import re

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def clean_row(row):
    return [re.sub(r'\s+', ' ', cell).strip() for cell in row]

def fill_empty_third_column(row):
    if len(row) > 2 and row[2] == '':
        row[2] = row[1]
    return row

def format_special_characters(row):
    formatted_row = []
    for cell in row:
        cell = re.sub(r'\s*-\s*', ' - ', cell)
        cell = re.sub(r'\s*/\s*', '/', cell)
        formatted_row.append(cell)
    return formatted_row

def read_file_with_encoding(file_path, encoding):
    with open(file_path, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        content = []
        for row in reader:
            cleaned_row = clean_row(row)
            filled_row = fill_empty_third_column(cleaned_row)
            formatted_row = format_special_characters(filled_row)
            content.append(formatted_row[:-1])
    return content

def write_to_new_file(file_path, content):
    new_file_path = file_path.replace('.csv', '.txt')
    with open(new_file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerows(content)
    return new_file_path

file_path = 'docs/export_helpdesk.csv'
encoding = detect_encoding(file_path)
file_content = read_file_with_encoding(file_path, encoding)
new_file_path = write_to_new_file(file_path, file_content)

print(f"O conteúdo foi escrito em {new_file_path}.")