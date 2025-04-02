import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def criar_driver(headless: bool = True) -> webdriver.Edge:
    options = webdriver.EdgeOptions()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    return driver


def salvar_codigo_fonte(driver: webdriver.Edge, url: str,
                        output_file: str = 'codigo_fonte.html', wait_time: int = 10) -> None:
    try:
        logging.info(f"Acessando URL: {url}")
        driver.get(url)

        WebDriverWait(driver, wait_time).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        codigo_fonte = driver.page_source

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(codigo_fonte)

        logging.info(f"Código-fonte salvo em: {output_file}")
    except Exception as e:
        logging.exception(f"Ocorreu um erro ao acessar a URL '{url}'.")


def main() -> None:
    url = 'https://example.com'
    try:
        with criar_driver(headless=False) as driver:
            salvar_codigo_fonte(driver, url=url)
    except Exception as e:
        logging.exception("Falha ao executar a função main.")


if __name__ == '__main__':
    main()