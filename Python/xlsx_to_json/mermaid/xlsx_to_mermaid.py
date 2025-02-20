def generate_mermaid_code(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines if line.strip()]
    node_map = {}
    node_counter = 0
    mermaid_code = "%%{init: {'theme': 'default', 'themeVariables': { 'primaryColor': '#ffffff', 'edgeColor': '#000000', 'nodeTextColor': '#000000'}}}%%\n\nflowchart LR\n\n"

    def get_node_variable(node_name):
        nonlocal node_counter
        if node_name not in node_map:
            node_map[node_name] = f"{node_counter:03}"
            node_counter += 1
        return node_map[node_name]

    for line in lines:
        if '-->' in line:
            source, target = line.split('-->')
            source = source.strip()
            target = target.strip()
            if source == "[]" or target == "[]":
                continue
            source_var = get_node_variable(source)
            target_var = get_node_variable(target)
            mermaid_code += f"{source_var}[{source[1:-1]}] --> {target_var}[{target[1:-1]}]\n"

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(mermaid_code)

file_path = 'a.txt'
output_path = 'fluxograma.mmd'

generate_mermaid_code(file_path, output_path)
print(f"Arquivo de saída: {output_path}")