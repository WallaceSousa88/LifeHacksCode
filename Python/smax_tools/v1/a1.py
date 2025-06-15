import re

from bs4 import BeautifulSoup

def gerar_sql_query(html_content):
    soup = None

    def extrair_data_id_modulo_unico(html_content):
        nonlocal soup
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            tag_com_id_modulo = soup.find(attrs={"data-idmodulo": True})
            if tag_com_id_modulo:
                return tag_com_id_modulo['data-idmodulo']
            else:
                return "0"
        except Exception as e:
            print(f"Ocorreu um erro ao processar o HTML: {e}")
            return "0"

    tarefa_id = extrair_data_id_modulo_unico(html_content)

    query = f"DECLARE @TAREA_ID INT = {tarefa_id};\n\n"
    query += "SELECT\n"
    query += "    C.DES_CATEGORIA,\n"
    query += "    B.DES_ITEM,\n"
    query += "    CE.DES_LEGENDA,\n"
    query += "    CE.DES_FORMATO,\n"
    query += "    CE.TAG_IS_REQUIRED,\n"
    query += "    CE.DES_LISTA,\n"
    query += "    CE.NUM_ORDEM,\n"
    query += "    CE.NUM_ID,\n"
    query += "    B.DES_AJUDA\n"
    query += "FROM\n"
    query += "    TITEM B\n"
    query += "LEFT JOIN\n"
    query += "    TCATEGORIA C ON B.NUM_ID_TCATEGORIA = C.NUM_ID\n"
    query += "LEFT JOIN\n"
    query += "    TCAMPOS_EXTRAS CE ON B.NUM_ID = CE.NUM_ID_TITEM\n"
    query += "WHERE\n"
    query += "    (C.NUM_ID_TAREA = @TAREA_ID)\n"
    query += "    AND (\n"

    conditions = []
    current_category = None

    def process_list(ul_element, indent_level=0):
        nonlocal query
        nonlocal conditions
        nonlocal current_category

        for li in ul_element.find_all('li', recursive=False):
            handle = li.find('div', class_='dd-handle')
            if handle:
                text_parts = []
                for child in handle.contents:
                    if child.name is None:
                        text_parts.append(child.strip())
                text = " ".join(filter(None, text_parts))
                text = re.sub(r'<[^>]*>', '', text)

                if indent_level == 0:
                    if current_category:
                        if conditions:
                            query += "      (\n"
                            query += '        ' + ' OR\n        '.join(conditions)
                            query += '\n      )\n      OR\n'
                        conditions = []
                    current_category = text.replace("'", "''")

                elif indent_level == 1:
                    escaped_text = text.replace("'", "''").replace('"', '')
                    conditions.append(f"B.DES_ITEM = '{escaped_text}' AND C.DES_CATEGORIA = '{current_category}'")

            sub_ol = li.find('ol', class_='dd-list')
            if sub_ol:
                process_list(sub_ol, indent_level + 1)

    main_ol = soup.find('div', id='mapa_nestable').find('ol', class_='dd-list')
    if main_ol:
        process_list(main_ol)

    if current_category and conditions:
        query += "      (\n"
        query += '        ' + ' OR\n        '.join(conditions)
        query += '\n      )\n'

    query += "    )\n"
    query += "ORDER BY\n"
    query += "    C.DES_CATEGORIA,\n"
    query += "    B.DES_ITEM"

    return query

if __name__ == '__main__':
    with open('docs/html_sol.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    sql_query = gerar_sql_query(html_content)

    with open('docs/querry_hd.sql', 'w', encoding='utf-8') as f:
        f.write(sql_query)
    print('Arquivo "querry_hd.sql" criado!')