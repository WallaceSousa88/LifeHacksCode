import pkg_resources
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

protected_packages = ['pip', 'setuptools', 'wheel']

packages_to_uninstall = [
    dist.project_name
    for dist in pkg_resources.working_set
    if dist.project_name not in protected_packages
]

logging.info(f"Pacotes a serem desinstalados: {', '.join(packages_to_uninstall)}")

for package in packages_to_uninstall:
    try:
        logging.info(f"Iniciando a desinstalação de: {package}")
        subprocess.run(['pip', 'uninstall', '-y', package], check=True, capture_output=True, text=True)
        logging.info(f"Pacote '{package}' desinstalado com sucesso.")
    except subprocess.CalledProcessError as e:
       logging.error(f"Erro ao desinstalar '{package}':\n{e.stderr}")
    except Exception as e:
        logging.error(f"Erro inesperado ao desinstalar '{package}':\n{e}")

logging.info("Processo de desinstalação finalizado.")