import requests
import json
import os
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

target_url = f"/rest/{tenant_id}/ems/Offering?layout=Id,DisplayLabel,OfferingType,Service,Status,Service.DisplayLabel,Service.IsDeleted&meta=totalCount&order=Id+asc&size=250&skip=0"

headers = {
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
    "x-xsrf-token": xsrf_token,
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "x-client-tenant-version": "v27",
    "x-requested-with": "XMLHttpRequest",
    "x-request-land": "Unknown",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": f"{login_url}saw/Offerings",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "priority": "u=1, i"
}

response = requests.get(f"{login_url}{target_url}",
                         headers=headers, cookies=selenium_cookies)

if response.status_code == 200:
    data = response.json()

    parsed_url = urlparse(target_url)
    path_parts = parsed_url.path.split("/")[1:-1]
    directory = os.path.join(os.getcwd(), *path_parts)
    os.makedirs(directory, exist_ok=True)

    filename = os.path.join(directory, parsed_url.path.split("/")[-1] + ".json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data['entities'], f, ensure_ascii=False, indent=4)

    print(f"Dados salvos em: {filename}")

else:
    print(f"Erro na requisição: {response.status_code}")

driver(quit)