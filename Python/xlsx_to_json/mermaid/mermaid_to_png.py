import subprocess

mermaid_file = 'fluxograma.mmd'
output_file = 'fluxograma.png'

command = f'mmdc -i {mermaid_file} -o {output_file} -b white -t default -H 1080 -w 1920'

subprocess.run(command, shell=True)