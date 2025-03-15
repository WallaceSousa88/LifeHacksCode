import logging

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def salvar_codigo_fonte(driver, url, output_file='codigo_fonte.html', wait_time=10):
    try:
        driver.get(url)

        WebDriverWait(driver, wait_time).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        codigo_fonte = driver.page_source
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(codigo_fonte)

        logging.info("Código-fonte salvo!")
    except Exception as e:
        logging.error(f"Ocorreu o erro: {e}")

def main():
    url = 'https://example.com'

    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)

    try:
        salvar_codigo_fonte(driver, url)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()