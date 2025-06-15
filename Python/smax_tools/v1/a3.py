import json
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

edge_driver_path = config['edge_driver_path']
url = config['url']

service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service)

def get_unique_values_from_csv(file_path):
    unique_values = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            unique_values.add(row['DES_CATEGORIA'])
    return list(unique_values)

csv_file_path = 'docs/export_helpdesk.txt'
unique_values = get_unique_values_from_csv(csv_file_path)

try:
    driver.get(url)

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username_field.send_keys('username')
    username_field.send_keys(Keys.ENTER)
    time.sleep(5)

    WebDriverWait(driver, 10).until(
        EC.url_changes(url)
    )
    time.sleep(5)

    driver.get(url + '/saw/scm')
    time.sleep(5)

    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@data-aid="add-btn-1"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
    add_button.click()
    time.sleep(3)

    input_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'new_DisplayLabel'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
    input_field.send_keys('aaa')
    time.sleep(3)

    description_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'new_Description'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", description_field)
    description_field.send_keys('aaa')
    time.sleep(3)

    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-aid="dialog-button-save"]'))
    )
    save_button.click()
    time.sleep(5)

    link_aqui = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[text()="aqui"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", link_aqui)
    link_aqui.click()
    time.sleep(5)

    for value in unique_values:
        new_display_label_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'new_DisplayLabel'))
        )
        new_display_label_field.send_keys(value)

        if value != unique_values[-1]:
            save_and_add_another_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-aid="dialog-button-save-and-add-another"]'))
            )
            save_and_add_another_button.click()
            time.sleep(3)
        else:
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-aid="dialog-button-save"]'))
            )
            save_button.click()
            time.sleep(5)

finally:
    driver.quit()