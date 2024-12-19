import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils import press_tab, press_enter, login, get_column_values1, transform_text

with open('../config.json', 'r') as config_file:
    config = json.load(config_file)

driver_path = config['chrome_driver_path']
url = config['url']
username = config['username']
email = config['email']
password = config['password']
offering = config['offering']

csv_file_path = '../export_helpdesk.txt'
second_column_values = sorted(list(set(get_column_values1(csv_file_path, 1))))
third_column_values = sorted(list(set(get_column_values1(csv_file_path, 2))))

column_mapping = {}
for second_value, third_value in zip(get_column_values1(csv_file_path, 1), get_column_values1(csv_file_path, 2)):
    if second_value not in column_mapping:
        column_mapping[second_value] = []
    column_mapping[second_value].append(third_value.strip())

common_fields = sorted(set.intersection(*[set(values) for values in column_mapping.values()]))
unique_mappings = {key: sorted(list(set(third_column_values) - set(values))) for key, values in column_mapping.items()}

grouped_rules = {}
for key, values in unique_mappings.items():
    transformed_key = transform_text(key)
    values_tuple = tuple(values)
    if values_tuple not in grouped_rules:
        grouped_rules[values_tuple] = []
    grouped_rules[values_tuple].append(transformed_key)

service = ChromeService(executable_path=driver_path)
options = ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

try:
    login(driver, url, username, email, password)

    driver.get(f"{url}/saw/Offering/{offering}/rules")
    time.sleep(5)

    render_forms_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@data-aid='rule-event-header']//span[text()='Renderizando formulários']"))
    )
    render_forms_element.click()
    time.sleep(3)

    add_rule_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-aid='add-after-btn-clickable']"))
    )
    add_rule_button.click()
    time.sleep(3)

    if_then_rule = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//li[@data-aid='rule-OnRendering-dslCondition']//a[text()='Regra \"If...Then\"']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", if_then_rule)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", if_then_rule)
    time.sleep(3)

    hide_fields_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-aid='HideMultipleFieldsRenderingTemplate.displayLabel']"))
    )
    hide_fields_option.click()
    time.sleep(3)
    press_tab(driver, 3)
    press_enter(driver)

    rule_parameter = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='default_dsl' and contains(text(), 'expressão')]"))
    )
    rule_parameter.click()
    time.sleep(3)

    code_mirror = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.CodeMirror-lines"))
    )
    code_mirror.click()
    time.sleep(2)

    condition_string = "${entity.UserOptions.SelecioneItemLista_c == 'Selecione_c'}"

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.CodeMirror-lines")))
    action = webdriver.ActionChains(driver)
    action.send_keys(condition_string).perform()
    press_tab(driver, 1)
    press_enter(driver)
    time.sleep(3)

    target_field_name = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='default_targetFieldName' and contains(text(), 'campos')]"))
    )
    target_field_name.click()
    time.sleep(3)

    for _ in third_column_values:
        add_item_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='addItem' and @ng-click='createRow()']"))
        )
        add_item_button.click()
        time.sleep(3)

    input_field_container = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-aid='fieldName']"))
    )
    input_field_container.click()

    input_field = input_field_container.find_element(By.CSS_SELECTOR, "input[type='hidden']")
    driver.execute_script("arguments[0].click();", input_field)
    time.sleep(1)

    for index, item in enumerate(third_column_values):
        action.send_keys(item).perform()
        press_enter(driver)

        if index < len(third_column_values) - 1:
            press_tab(driver, 1)
        else:
            press_tab(driver, 1)
            press_enter(driver)

        time.sleep(3)

    for fields, keys in grouped_rules.items():
        add_rule_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-aid='add-after-btn-clickable']"))
        )
        add_rule_button.click()
        time.sleep(3)

        if_then_rule = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//li[@data-aid='rule-OnRendering-dslCondition']//a[text()='Regra \"If...Then\"']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", if_then_rule)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", if_then_rule)
        time.sleep(3)

        hide_fields_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-aid='HideMultipleFieldsRenderingTemplate.displayLabel']"))
        )
        hide_fields_option.click()
        time.sleep(3)
        press_tab(driver, 3)
        press_enter(driver)

        rule_parameter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='default_dsl' and contains(text(), 'expressão')]"))
        )
        rule_parameter.click()
        time.sleep(3)

        code_mirror = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.CodeMirror-lines"))
        )
        code_mirror.click()
        time.sleep(2)

        condition_string = " || ".join([f"${{entity.UserOptions.SelecioneItemLista_c == '{key}_c'}}" for key in keys])

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.CodeMirror-lines")))
        action = webdriver.ActionChains(driver)
        action.send_keys(condition_string).perform()
        press_tab(driver, 1)
        press_enter(driver)
        time.sleep(3)

        target_field_name = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='default_targetFieldName' and contains(text(), 'campos')]"))
        )
        target_field_name.click()
        time.sleep(3)

        for _ in fields:
            add_item_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='addItem' and @ng-click='createRow()']"))
            )
            add_item_button.click()
            time.sleep(3)

        input_field_container = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-aid='fieldName']"))
        )
        input_field_container.click()

        input_field = input_field_container.find_element(By.CSS_SELECTOR, "input[type='hidden']")
        driver.execute_script("arguments[0].click();", input_field)
        time.sleep(1)

        for index, item in enumerate(fields):
            item = item.split('?')[0]

            if len(item) > 100:
                item = item[:100]

            action.send_keys(item).perform()
            press_enter(driver)

            if index < len(fields) - 1:
                press_tab(driver, 1)
            else:
                press_tab(driver, 1)
                press_enter(driver)

            time.sleep(3)

    time.sleep(5)
    save_button = driver.find_element(By.XPATH, "//span[@class='icon-save pl-toolbar-item-icon']")
    save_button.click()
    time.sleep(120)

finally:
    driver.quit()