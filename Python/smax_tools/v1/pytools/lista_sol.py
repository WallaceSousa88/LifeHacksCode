import re

from bs4 import BeautifulSoup

def extrair_lista_aninhada(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    output = ""
    first_item = True

    def process_list(ul_element, indent_level=0):
        nonlocal output
        nonlocal first_item
        for li in ul_element.find_all('li', recursive=False):

            handle = li.find('div', class_='dd-handle')
            if handle:

                if indent_level == 0:
                  if not first_item:
                      output += "\n"
                  first_item = False

                text_parts = []
                for child in handle.contents:
                    if child.name is None:
                        text_parts.append(child.strip())
                text = " ".join(filter(None, text_parts))
                text = re.sub(r'<[^>]*>', '', text)
                output += ("  " * indent_level) + text + "\n"

            sub_ol = li.find('ol', class_='dd-list')
            if sub_ol:
                process_list(sub_ol, indent_level + 1)

    main_ol = soup.find('div', id='mapa_nestable').find('ol', class_='dd-list')
    if main_ol:
        process_list(main_ol)

    return output

if __name__ == '__main__':
    with open('../docs/html_sol.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    lista_extraida = extrair_lista_aninhada(html_content)
    with open('lista_sol.txt', 'w', encoding='utf-8') as f:
        f.write(lista_extraida)
    print('Arquivo "lista_sol.txt" criado!')