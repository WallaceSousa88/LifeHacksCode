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

def kill_edge_processes():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Não há processos do Edge para encerrar: {e}")

def login():
    kill_edge_processes()
    subprocess.Popen(["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    edge_driver_path = config['edge_driver_path']
    url = config['url']

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