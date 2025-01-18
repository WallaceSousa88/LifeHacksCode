import time
import subprocess
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

def login():
    subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], check=False, capture_output=True)
    subprocess.Popen(["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    edge_driver_path = "C:\\edgedriver_win64\\msedgedriver.exe"
    url = "https://csc-dev.cemig.com.br"

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

    next_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'next'))
        )
    next_button.click()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.main-toolbar-icon-wrapper[role="button"][ng-click="showRecentConversations()"]'))
    )

    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    driver.minimize_window()
    return session

if __name__ == '__main__':
    session = login()
    print("Sessão criada com sucesso!")