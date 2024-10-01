import json
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path , 'r') as config_file:
    config = json.load(config_file)

driver_selenium = config['driver_selenium']
login_url = config['login_url']
matricula = config['matricula']

service = webdriver.edge.service.Service(executable_path=driver_selenium)
driver = webdriver.Edge(service=service)
driver.maximize_window()
driver.get(f"{login_url}saw/Offering/44400/userOption")
time.sleep(5)

username_field = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "username"))
)
username_field.send_keys(matricula)
time.sleep(1)
username_field.send_keys(Keys.ENTER)
time.sleep(5)

with open("novos_itens_denuncia.txt", "r", encoding="utf-8") as f:
    itens = f.read().splitlines()

contato_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(), 'Nome Completo')]")
    )
)
driver.execute_script("arguments[0].click();", contato_element)

actions = ActionChains(driver)
actions.send_keys(Keys.PAGE_DOWN).perform()
time.sleep(2)

contato_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(), 'Motivo do Contato')]")
    )
)
driver.execute_script("arguments[0].click();", contato_element)

time.sleep(5)

adicionar_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-aid='tool-bar-btn-additem']"))
)

actions = ActionChains(driver)
actions.move_to_element(adicionar_button).click().perform()

time.sleep(5)

for index, item in enumerate(itens):
    nome_interno, nome_exibicao = item.split(";")

    nome_interno_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "_name"))
    )
    nome_interno_field.send_keys(nome_interno)

    time.sleep(3)

    nome_exibicao_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#displayNameHeaderInputDiag2 input"))
    )
    nome_exibicao_field.send_keys(nome_exibicao)

    time.sleep(3)

    if index < len(itens) - 1:
        adicionar_outro_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Adicionar outro')]"))
        )
        WebDriverWait(driver, 20).until(lambda driver: adicionar_outro_button.is_enabled())
        adicionar_outro_button.click()
        time.sleep(3)
    else:
        ok_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        )
        ok_button.click()

time.sleep(120)
driver.quit()