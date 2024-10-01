import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from urllib.parse import urlparse

with open('config.json' , 'r') as config_file:
    config = json.load(config_file)

login_url = config['login_url']
tenant_id = config['tenant_id']
matricula = config['matricula']
driver_selenium = config['driver_selenium']

edge_options = Options()
service = Service(driver_selenium)
driver = webdriver.Edge(service=service, options=edge_options)
driver.get(login_url)
driver.maximize_window()

username_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "username"))
)

username_field.send_keys(matricula)
time.sleep(1)

next_button = driver.find_element(By.ID, "next")
next_button.click()
time.sleep(5)

cookies = driver.get_cookies()
for cookie in cookies:
    if cookie['name'] in ['XSRF-TOKEN', 'SMAX_AUTH_TOKEN', 'JSESSIONID']:
        print(f"Cookie: {cookie['name']}, Valor: {cookie['value']}")

edge_options.add_argument("start-minimized")

cookies = driver.get_cookies()
selenium_cookies = {}
for cookie in cookies:
    selenium_cookies[cookie['name']] = cookie['value']

xsrf_token = selenium_cookies['XSRF-TOKEN']
smax_auth_token = selenium_cookies['SMAX_AUTH_TOKEN']

target_url = f""

headers = {
    "" : ""
}

response = requests.get(f"{login_url}{target_url}",
                         headers=headers, cookies=selenium_cookies)

driver(quit)