import json
import csv
import time
import re
import unicodedata

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

with open('../config.json', 'r') as config_file:
    config = json.load(config_file)

chrome_driver_path = config['chrome_driver_path']
url = config['url']
username = config['username']
email = config['email']
password = config['password']
offering = config['offering']

service = ChromeService(executable_path=chrome_driver_path)
options = ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

def get_column_values(file_path, column_index):
    values = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            values.append(row[column_index].strip('\"'))
    return values

def transform_text(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = text.replace('ç', 'c').replace('Ç', 'C')
    text = re.sub(r'[^A-Za-z0-9]', '', text)
    if text and not text[0].isalpha():
        text = 'A' + text
    return text

def press_tab(times=1):
    for _ in range(times):
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(1)

def press_enter():
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    time.sleep(5)

def is_boolean_list(items):
    normalized_items = [unicodedata.normalize('NFKD', item).encode('ASCII', 'ignore').decode('ASCII').lower() for item in items]
    return set(normalized_items) == {'sim', 'nao'}

csv_file_path = '../export_helpdesk.txt'
second_column_values = sorted(list(set(get_column_values(csv_file_path, 1))))
third_column_values = get_column_values(csv_file_path, 2)
fifth_column_values = get_column_values(csv_file_path, 4)
sixth_column_values = get_column_values(csv_file_path, 5)

try:
    driver.get(url)
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(5)
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'i0116'))
    )
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)
    time.sleep(5)
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'i0118'))
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(25)
    offer_url = f"{url}/saw/Offering/{offering}/userOption"
    driver.get(offer_url)
    time.sleep(3)
    add_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Novo campo']"))
    )
    add_icon.click()
    time.sleep(3)
    press_enter()
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-aid=\"_localized_label_key\"]'))
    )
    input_field.send_keys('Selecione um item da lista')
    time.sleep(3)
    press_enter()
    press_tab(2)
    webdriver.ActionChains(driver).send_keys('Lista').perform()
    time.sleep(3)
    press_enter()
    add_button = driver.find_element(By.CSS_SELECTOR, 'button[data-aid=\"uo-create-list\"]')
    add_button.click()
    time.sleep(3)
    modal_input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
    )
    list_text = f'List{offering}'
    modal_input_field.send_keys(list_text)
    time.sleep(2)
    press_tab()
    webdriver.ActionChains(driver).send_keys(list_text).perform()
    time.sleep(2)
    press_tab(2)
    press_enter()
    add_item_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Adicionar']"))
    )
    add_item_button.click()
    modal_input_field_2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
    )
    modal_input_field_2.send_keys('Selecione')
    time.sleep(2)
    press_tab()
    webdriver.ActionChains(driver).send_keys('Selecione um item da lista').perform()
    time.sleep(2)
    press_tab(4)
    press_enter()
    for i, value in enumerate(second_column_values):
        modal_input_field_2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
        )
        transformed_value = transform_text(value)
        modal_input_field_2.send_keys(transformed_value)
        time.sleep(2)
        press_tab()
        webdriver.ActionChains(driver).send_keys(value).perform()
        time.sleep(2)
        if i == len(second_column_values) - 1:
            press_tab(3)
            press_enter()
        else:
            press_tab(4)
            press_enter()
    checkbox = driver.find_element(By.CSS_SELECTOR, 'span.checkboxInputSimulator')
    checkbox.click()
    time.sleep(2)
    for i in range(len(third_column_values)):
        add_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Novo campo']"))
        )
        add_icon.click()
        time.sleep(3)
        press_enter()
        if fifth_column_values[i] == 'True':
            checkbox = driver.find_element(By.CSS_SELECTOR, 'span.checkboxInputSimulator')
            checkbox.click()
            time.sleep(2)
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-aid=\"_localized_label_key\"]'))
        )
        input_field.send_keys(third_column_values[i])
        time.sleep(3)
        press_enter()
        if sixth_column_values[i]:
            press_tab(2)
            webdriver.ActionChains(driver).send_keys('Lista').perform()
            time.sleep(3)
            press_enter()
            items = sixth_column_values[i].split(';')
            if len(items) == 2 and is_boolean_list(items):
                press_tab(6)
                press_enter()
                webdriver.ActionChains(driver).send_keys('Booleano').perform()
                press_tab()
            else:
                add_button = driver.find_element(By.CSS_SELECTOR, 'button[data-aid=\"uo-create-list\"]')
                add_button.click()
                time.sleep(3)
                modal_input_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
                )
                list_text_aux = f'{list_text}aux{i+1}'
                modal_input_field.send_keys(list_text_aux)
                time.sleep(2)
                press_tab()
                webdriver.ActionChains(driver).send_keys(list_text_aux).perform()
                time.sleep(2)
                press_tab(2)
                press_enter()
                add_item_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Adicionar']"))
                )
                add_item_button.click()
                for j, item in enumerate(items):
                    modal_input_field_2 = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#_name'))
                    )
                    transformed_item = transform_text(item)
                    modal_input_field_2.send_keys(transformed_item)
                    time.sleep(2)
                    press_tab()
                    webdriver.ActionChains(driver).send_keys(item).perform()
                    time.sleep(2)
                    if j == len(items) - 1:
                        press_tab(3)
                        press_enter()
                    else:
                        press_tab(4)
                        press_enter()
    time.sleep(10)
finally:
    driver.quit()