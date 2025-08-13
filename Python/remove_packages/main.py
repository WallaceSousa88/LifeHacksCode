import importlib.metadata
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

protected_packages = {'pip', 'setuptools', 'wheel'}

installed_packages = {
    dist.metadata['Name'] for dist in importlib.metadata.distributions()
    if dist.metadata['Name'] not in protected_packages
}

logging.info(f"Pacotes a serem desinstalados: {', '.join(installed_packages)}")

success_count = 0
failure_count = 0

if installed_packages:
    try:
        result = subprocess.run(
            ['python', '-m', 'pip', 'uninstall', '-y', *installed_packages],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info("Desinstalação concluída com sucesso.")
        logging.info(result.stdout)
        success_count = len(installed_packages)
    except subprocess.CalledProcessError as e:
        logging.error("Erro na desinstalação em lote:")
        logging.error(e.stderr)
        failure_count = len(installed_packages)
else:
    logging.info("Nenhum pacote para desinstalar.")

logging.info(f"Resumo: {success_count} pacotes desinstalados com sucesso, {failure_count} falhas.")
