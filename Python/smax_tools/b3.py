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

def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length]
    return text

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
second_column_values = sorted(list(set(get_column_values1(csv_file_path, 1))))
third_column_values = sorted(list(set(get_column_values1(csv_file_path, 2))))

column_mapping = {}
for second_value, third_value in zip(get_column_values1(csv_file_path, 1), get_column_values1(csv_file_path, 2)):
    if second_value not in column_mapping:
        column_mapping[second_value] = []
    column_mapping[second_value].append(third_value.strip())

common_fields = sorted(set.intersection(*[set(values) for values in column_mapping.values()]))
unique_mappings = {key: sorted(list(set(third_column_values) - set(values))) for key, values in column_mapping.items()}

all_fields = set(third_column_values)
items_with_all_fields = [key for key, values in column_mapping.items() if set(values) == all_fields]

unique_mappings_filtered = {key: values for key, values in unique_mappings.items() if key not in items_with_all_fields}

grouped_rules = {}
for key, values in unique_mappings_filtered.items():
    transformed_key = transform_text(key)
    values_tuple = tuple(values)
    if values_tuple not in grouped_rules:
        grouped_rules[values_tuple] = []
    grouped_rules[values_tuple].append(transformed_key)

try:
    driver.get(f"{url}/saw/Offering/{offering}/rules")
    time.sleep(2)

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username_field.send_keys('username')
    username_field.send_keys(Keys.RETURN)

    render_forms_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@data-aid='rule-event-header']//span[text()='Renderizando formulários']"))
    )
    render_forms_element.click()
    time.sleep(1)

    add_rule_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-aid='add-after-btn-clickable']"))
    )
    add_rule_button.click()
    time.sleep(1)

    if_then_rule = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//li[@data-aid='rule-OnRendering-dslCondition']//a[text()='Regra \"If...Then\"']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", if_then_rule)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", if_then_rule)
    time.sleep(1)

    hide_fields_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-aid='HideMultipleFieldsRenderingTemplate.displayLabel']"))
    )
    hide_fields_option.click()
    time.sleep(1)
    press_tab(driver, 3)
    press_enter(driver)

    rule_parameter = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='default_dsl' and contains(text(), 'expressão')]"))
    )
    rule_parameter.click()
    time.sleep(1)

    code_mirror = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.CodeMirror-lines"))
    )
    code_mirror.click()
    time.sleep(1)

    condition_string = "${entity.UserOptions.SelecioneItemLista_c == 'Selecione_c'}"

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.CodeMirror-lines")))
    action = webdriver.ActionChains(driver)
    action.send_keys(condition_string).perform()
    press_tab(driver, 1)
    press_enter(driver)
    time.sleep(1)

    target_field_name = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='default_targetFieldName' and contains(text(), 'campos')]"))
    )
    target_field_name.click()
    time.sleep(1)

    for _ in third_column_values:
        add_item_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='addItem' and @ng-click='createRow()']"))
        )
        add_item_button.click()
        time.sleep(1)

    input_field_container = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-aid='fieldName']"))
    )
    input_field_container.click()

    input_field = input_field_container.find_element(By.CSS_SELECTOR, "input[type='hidden']")
    driver.execute_script("arguments[0].click();", input_field)
    time.sleep(1)

    for index, item in enumerate(third_column_values):
        item = item.split('?')[0]
        if len(item) > 100:
            item = item[:100]
            action.send_keys(item).perform()
            press_enter(driver)

        action.send_keys(item).perform()
        press_enter(driver)

        if index < len(third_column_values) - 1:
            press_tab(driver, 1)
        else:
            press_tab(driver, 1)
            press_enter(driver)

        time.sleep(1)

    for fields, keys in grouped_rules.items():
        add_rule_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-aid='add-after-btn-clickable']"))
        )
        add_rule_button.click()
        time.sleep(1)

        if_then_rule = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//li[@data-aid='rule-OnRendering-dslCondition']//a[text()='Regra \"If...Then\"']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", if_then_rule)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", if_then_rule)
        time.sleep(1)

        hide_fields_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-aid='HideMultipleFieldsRenderingTemplate.displayLabel']"))
        )
        hide_fields_option.click()
        time.sleep(1)
        press_tab(driver, 3)
        press_enter(driver)

        rule_parameter = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='default_dsl' and contains(text(), 'expressão')]"))
        )
        rule_parameter.click()
        time.sleep(1)

        code_mirror = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.CodeMirror-lines"))
        )
        code_mirror.click()
        time.sleep(1)

        condition_string = " || ".join([f"${{entity.UserOptions.SelecioneItemLista_c == '{truncate_text(key, 55)}_c'}}" for key in keys])

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.CodeMirror-lines")))
        action = webdriver.ActionChains(driver)
        action.send_keys(condition_string).perform()
        press_tab(driver, 1)
        press_enter(driver)
        time.sleep(1)

        target_field_name = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='default_targetFieldName' and contains(text(), 'campos')]"))
        )
        target_field_name.click()
        time.sleep(1)

        for _ in fields:
            add_item_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-aid='addItem' and @ng-click='createRow()']"))
            )
            add_item_button.click()
            time.sleep(1)

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

            time.sleep(1)
    save_button = driver.find_element(By.XPATH, "//span[@class='icon-save pl-toolbar-item-icon']")
    save_button.click()
finally:
    driver.quit()