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
from pytools.utils import get_column_values, transform_text, press_tab, press_enter, is_boolean_list

def kill_edge_processes():
    subprocess.call(["taskkill", "/F", "/IM", "msedge.exe"])

kill_edge_processes()
subprocess.Popen(["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "--remote-debugging-port=9222"])

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
third_column_values = get_column_values(csv_file_path, 2)
fourth_column_values = get_column_values(csv_file_path, 3)
fifth_column_values = get_column_values(csv_file_path, 4)
sixth_column_values = get_column_values(csv_file_path, 5)

combined_values = sorted(set(zip(third_column_values, fourth_column_values, fifth_column_values, sixth_column_values)))

field_name_counts = {}
list_name_counts = {}

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
    time.sleep(10)

    for i, (value, formato, is_required, lista) in enumerate(combined_values):
        add_icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Novo campo']"))
        )
        add_icon.click()

        ok_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-aid="dialog-button-ok"]'))
        )
        ok_button.click()

        time.sleep(3)
        input_field_name = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "propertyGrid_name"))
        )
        input_field_name.click()
        input_field_name.send_keys(Keys.CONTROL + 'a')
        input_field_name.send_keys(Keys.BACKSPACE)

        transformed_value = transform_text(value)

        if transformed_value in field_name_counts:
            field_name_counts[transformed_value] += 1
            transformed_value = f"{transformed_value}{field_name_counts[transformed_value]}"
        else:
            field_name_counts[transformed_value] = 0

        input_field_name.send_keys(transformed_value)
        time.sleep(3)

        input_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-aid="_localized_label_key"]'))
        )
        input_field.send_keys(value)
        time.sleep(2)

        formato = formato.strip()

        if formato == 'NENHUM':
            pass
        elif len(formato.strip()) == 19:
            press_tab(driver, 2)
            webdriver.ActionChains(driver).send_keys('DataHora').perform()
            press_enter(driver)
        elif len(formato.strip()) == 10:
            press_tab(driver, 2)
            webdriver.ActionChains(driver).send_keys('Data').perform()
            press_enter(driver)

        if lista:
            press_tab(driver, 2)
            webdriver.ActionChains(driver).send_keys('Lista').perform()
            press_enter(driver)
            items = lista.split(';')
            if len(items) == 2 and is_boolean_list(items):
                press_tab(driver, 6)
                press_enter(driver)
                webdriver.ActionChains(driver).send_keys('Booleano').perform()
                press_enter(driver)
            else:
                add_button = driver.find_element(By.CSS_SELECTOR, 'button[data-aid="uo-create-list"]')
                add_button.click()
                modal_input_field = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
                )

                list_text_aux_base = f'ListaOffer{offering}aux'
                if list_text_aux_base in list_name_counts:
                    list_name_counts[list_text_aux_base] += 1
                    list_text_aux = f"{list_text_aux_base}{list_name_counts[list_text_aux_base]}"
                else:
                    list_name_counts[list_text_aux_base] = 0
                    list_text_aux = list_text_aux_base

                modal_input_field.send_keys(list_text_aux)
                press_tab(driver)
                webdriver.ActionChains(driver).send_keys(list_text_aux).perform()
                press_tab(driver, 2)
                press_enter(driver)
                add_item_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Adicionar']"))
                )
                add_item_button.click()
                for j, item in enumerate(items):
                    modal_input_field_2 = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
                    )
                    transformed_item = transform_text(item)
                    modal_input_field_2.send_keys(transformed_item)
                    press_tab(driver)
                    webdriver.ActionChains(driver).send_keys(item).perform()
                    if j == len(items) - 1:
                        press_tab(driver, 3)
                        press_enter(driver)
                    else:
                        press_tab(driver, 4)
                        press_enter(driver)

        if is_required.lower() == 'true':
            checkbox = driver.find_element(By.CSS_SELECTOR, 'span.checkboxInputSimulator')
            checkbox.click()

    save_button = driver.find_element(By.XPATH, "//span[@class='icon-save pl-toolbar-item-icon']")
    save_button.click()
finally:
    driver.quit()