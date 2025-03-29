import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def salvar_codigo_fonte(driver: webdriver.Edge, url: str, output_file: str = 'codigo_fonte.html', wait_time: int = 10) -> None:
    try:
        driver.get(url)
        WebDriverWait(driver, wait_time).until(lambda d: d.execute_script("return document.readyState") == "complete")
        codigo_fonte = driver.page_source
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(codigo_fonte)
        logging.info("Código-fonte salvo!")
    except Exception as e:
        logging.error(f"Ocorreu o erro: {e}")

def main() -> None:
    url: str = 'https://example.com'
    service: Service = Service(EdgeChromiumDriverManager().install())
    with webdriver.Edge(service=service) as driver:
        salvar_codigo_fonte(driver, url)

if __name__ == '__main__':
    main()