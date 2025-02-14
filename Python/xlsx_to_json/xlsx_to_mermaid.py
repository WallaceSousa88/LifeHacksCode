import pandas as pd
import re

def sanitize_text(text):
    text = re.sub(r'[\(\)]', '', text)
    text = text.replace(';', ',')
    return text.strip()

def generate_mermaid_code(filename):
    df = pd.read_excel(filename)
    mermaid_code = "graph LR\n"
    relations = set()
    node_map = {}

    for col_index in range(len(df.columns)):
        unique_values = df[df.columns[col_index]].dropna().unique()
        for idx, value in enumerate(unique_values):
            node_key = f"COL{col_index + 1}_{idx}"
            node_map[value] = node_key
            mermaid_code += f"{node_key}[{sanitize_text(value)}]\n"

    for index, row in df.iterrows():
        for i in range(len(df.columns) - 1):
            if pd.notna(row[i]) and pd.notna(row[i + 1]):
                node1 = node_map[row[i]]
                node2 = node_map[row[i + 1]]
                relation = f"{node1} --> {node2}"
                relations.add(relation)

    for relation in relations:
        mermaid_code += f"{relation}\n"

    return mermaid_code

def save_mermaid_code_to_file(filename, code):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(code)

input_filename = "seu_arquivo.xlsx"
output_filename = "mermaid_code.txt"

mermaid_code = generate_mermaid_code(input_filename)
save_mermaid_code_to_file(output_filename, mermaid_code)

print(f"Código Mermaid salvo em {output_filename}")
