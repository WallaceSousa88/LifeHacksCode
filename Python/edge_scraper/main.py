import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

url = 'https://example.com'

try:
    driver.get(url)

    time.sleep(5)

    codigo_fonte = driver.page_source
    with open('codigo_fonte.html', 'w', encoding='utf-8') as file:
        file.write(codigo_fonte)

    print("Código-fonte salvo com sucesso!")
finally:
    driver.quit()