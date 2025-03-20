def replace_words(text):
    words_to_replace = {
    'De': 'de',
    'Do': 'do',
    'Da': 'da',
    'Dos': 'dos',
    'Das': 'das',
    'E': 'e',
    'Em': 'em',
    'A': 'a',
    'As': 'as',
    'À': 'à',
    'Às': 'às',
    'Á': 'á',
    'Ás': 'ás',
    'Ao': 'ao',
    'O': 'o',
    'Ou': 'ou',
    'Os': 'os',
    'Que': 'que',
    'Um': 'um',
    'Uma': 'uma',
    'Uns': 'uns',
    'Umas': 'umas',
    'Para': 'para',
    'Por': 'por',
    'Como': 'como',
    'Com': 'com',
    'Se': 'se',
    'Mas': 'mas',
    'Ainda': 'ainda',
    'Embora': 'embora',
    'Nem': 'nem',
    'Logo': 'logo',
    'Pois': 'pois',
    'Porque': 'porque',
    'Portanto': 'portanto',
    'Contudo': 'contudo',
    'Todavia': 'todavia',
    'Entretanto': 'entretanto',
    'Além': 'além',
    'Apesar': 'apesar',
    'Conforme': 'conforme',
    'Desde': 'desde',
    'Depois': 'depois',
    'Durante': 'durante',
    'Até': 'até',
    'Entre': 'entre',
    'Sob': 'sob',
    'Sobre': 'sobre',
    'Contra': 'contra',
    'Sem': 'sem',
    'Mediante': 'mediante',
    'Segundo': 'segundo',
    'Atrás': 'atrás',
    'Diante': 'diante',
    'Perante': 'perante',
    'Trás': 'trás'
}

    for word, replacement in words_to_replace.items():
        text = text.replace(f' {word} ', f' {replacement} ')

    return text

with open('in.txt', 'r', encoding='utf-8') as file:
    input_text = file.read()

output_text = replace_words(input_text)

with open('out.txt', 'w', encoding='utf-8') as file:
    file.write(output_text)

print("Finalizado!")