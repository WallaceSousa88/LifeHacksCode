# pip install pandas mermaid

import pandas as pd

df = pd.read_excel('x.xlsx')

flowchart = "graph TD\n"
levels = df.columns

for index, row in df.iterrows():
    nodes = [f"{levels[i]}_{row[i]}" for i in range(len(levels))]
    for i in range(len(nodes) - 1):
        flowchart += f"{nodes[i]} --> {nodes[i+1]}\n"

with open('fluxograma.mmd', 'w') as file:
    file.write(flowchart)

print("Fluxograma gerado!")