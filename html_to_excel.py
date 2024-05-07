# pip install beautifulsoup4
# pip install pandas
# pip install openpyxl

# pip install beautifulsoup4 pandas openpyxl

from bs4 import BeautifulSoup
import re
import pandas as pd

html_file_path = input('Digite o caminho do arquivo HTML: ')

with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

last_update_divs = soup.find_all('div', style='text-align:left;')

machine_names_list = []
last_updates_list = []

for update_div in last_update_divs:
    machine_name = update_div.find_previous('h2', class_='fs-4 fw-bold').get_text(strip=True)
    last_update_tag = update_div.find('p')
    
    if last_update_tag:
        last_update = last_update_tag.get_text(strip=True)
        last_update = re.sub(r'\.\d+', '', last_update)
        machine_names_list.append(machine_name)
        last_updates_list.append(last_update)

data = {'Nome da Máquina': machine_names_list, 'Última Atualização': last_updates_list}
df = pd.DataFrame(data)

output_excel_path = input('Digite o local de saída para o arquivo Excel: ')
df.to_excel(output_excel_path, index=False)

print(f"Os resultados foram salvos em '{output_excel_path}'.")
