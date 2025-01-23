import json
import time
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from pytools.utils import get_column_values1, transform_text, press_tab, press_enter, kill_edge_processes

kill_edge_processes()
subprocess.Popen(["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "--remote-debugging-port=9222"])
time.sleep(5)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

edge_driver_path = config['edge_driver_path']
url = config['url']
offering = config['offering']

service = EdgeService(executable_path=edge_driver_path)
options = EdgeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Edge(service=service, options=options)

csv_file_path = 'docs/export_helpdesk.txt'
second_column_values = sorted(set(get_column_values1(csv_file_path, 1)), key=lambda x: x.lower())

try:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

    url = f"{url}/saw/Offering/{offering}/userOption"

    driver.get(url)
    username_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username_field.send_keys('username')
    username_field.send_keys(Keys.RETURN)

    add_icon = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Novo campo']"))
    )
    add_icon.click()
    time.sleep(3)
    press_enter(driver)

    input_field_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "propertyGrid_name"))
    )

    input_field_name.click()
    input_field_name.send_keys(Keys.CONTROL + 'a')
    input_field_name.send_keys(Keys.BACKSPACE)
    input_field_name.send_keys('SelecioneItemLista')
    time.sleep(3)

    input_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-aid=\"_localized_label_key\"]'))
    )
    input_field.send_keys('Selecione um item da lista')
    time.sleep(3)
    press_enter(driver)
    press_tab(driver, 2)
    webdriver.ActionChains(driver).send_keys('Lista').perform()
    time.sleep(3)
    press_enter(driver)

    add_button = driver.find_element(By.CSS_SELECTOR, 'button[data-aid=\"uo-create-list\"]')
    add_button.click()
    time.sleep(3)

    modal_input_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
    )
    list_text = f'ListaOffer{offering}'
    modal_input_field.send_keys(list_text)
    time.sleep(2)
    press_tab(driver)
    webdriver.ActionChains(driver).send_keys(list_text).perform()
    time.sleep(2)
    press_tab(driver, 2)
    press_enter(driver)

    add_item_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Adicionar']"))
    )
    add_item_button.click()

    modal_input_field_2 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
    )
    modal_input_field_2.send_keys('Selecione')
    time.sleep(2)
    press_tab(driver)
    webdriver.ActionChains(driver).send_keys('Selecione um item da lista').perform()
    time.sleep(2)
    press_tab(driver, 4)
    press_enter(driver)

    for i, value in enumerate(second_column_values):
        modal_input_field_2 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
        )
        transformed_value = transform_text(value)
        modal_input_field_2.send_keys(transformed_value)
        time.sleep(2)
        press_tab(driver)
        webdriver.ActionChains(driver).send_keys(value).perform()
        time.sleep(2)
        if i == len(second_column_values) - 1:
            press_tab(driver, 3)
            press_enter(driver)
        else:
            press_tab(driver, 4)
            press_enter(driver)

    checkbox = driver.find_element(By.CSS_SELECTOR, 'span.checkboxInputSimulator')
    checkbox.click()
    save_button = driver.find_element(By.XPATH, "//span[@class='icon-save pl-toolbar-item-icon']")
    save_button.click()
finally:
    driver.quit()