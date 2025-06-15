import os
import json
import time
import subprocess
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

url = config['url']
offer_id = config['offering']
edge_driver_path = config['edge_driver_path']

def kill_edge_processes():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Não há processos do Edge para encerrar: {e}")

def login():
    kill_edge_processes()
    subprocess.Popen(["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    service = EdgeService(executable_path=edge_driver_path)
    options = EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Edge(service=service, options=options)

    driver.get(f"{url}")

    username_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username_field.send_keys('username')
    username_field.send_keys(Keys.RETURN)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.main-toolbar-icon-wrapper[role="button"][ng-click="showRecentConversations()"]'))
    )

    return driver

def get_session_from_driver(driver):
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
    return session

temp_dir = os.path.join(os.getcwd(), 'temp')
os.makedirs(temp_dir, exist_ok=True)

json_file_path = os.path.join(temp_dir, "create_user_field_responses.json")

driver = login()
session = get_session_from_driver(driver)

create_field_url = f"{url}rest/549110341/l10n/bundle/user_options_metadata_messages/resource"
headers = {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json;charset=UTF-8",
    "x-xsrf-token": session.cookies.get("XSRF-TOKEN")
}

labels = {
    "en": "label1",
    "pt-BR": "label2"
}

payload = {
    "Values": labels
}

response = session.post(create_field_url, headers=headers, json=payload)
field_creation_response = response.json()

update_offer_url = f"{url}rest/549110341/ems/bulk"
field_name = field_creation_response.get("field_name", "")

update_payload = {
    "entities": [
        {
            "entity_type": "Offering",
            "properties": {
                "Id": offer_id,
                "UserOptionsName": field_name
            }
        }
    ],
    "operation": "UPDATE"
}

update_response = session.post(update_offer_url, headers=headers, json=update_payload)
offer_update_response = update_response.json()

with open(json_file_path, 'w') as json_file:
    json.dump({
        "field_creation_response": field_creation_response,
        "offer_update_response": offer_update_response
    }, json_file, indent=4)

driver.minimize_window()
driver.quit()

print(f"As respostas do servidor foram salvas em {json_file_path}")