import json
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

with open('..\\config.json', 'r') as config_file:
    config = json.load(config_file)

URL = config['url']
DEBUG_PORT = 9222

def get_session_and_login():
    edge_process = subprocess.Popen([
        "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        f"--remote-debugging-port={DEBUG_PORT}",
        "--user-data-dir=C:\\Temp\\EdgeProfile",
        "--disable-features=msEdgeSync"
    ])

    edge_service = EdgeService(EdgeChromiumDriverManager().install())
    options = EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("debuggerAddress", f"localhost:{DEBUG_PORT}")
    driver = webdriver.Edge(service=edge_service, options=options)

    driver.get(URL)

    username_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "username")))
    username_field.send_keys("username")

    next_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "next")))
    next_button.click()

    return driver, edge_process

if __name__ == "__main__":
    driver, edge_process = get_session_and_login()