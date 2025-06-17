# pip install selenium webdriver-manager

import os
import time
import subprocess

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def kill_edge_processes():
    for proc in ("msedge.exe", "msedgedriver.exe"):
        subprocess.run(
            ["taskkill", "/F", "/IM", proc],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def wait_for_element(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )

def automate_login():
    kill_edge_processes()

    edge_binary = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    user_data_dir = os.path.expandvars(r"%USERPROFILE%\AppData\Local\Microsoft\Edge\User Data")
    profile_name  = "Default"

    options = EdgeOptions()
    options.binary_location = edge_binary
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_name}")
    options.add_argument("--start-maximized")

    service = EdgeService(EdgeChromiumDriverManager().install())
    driver  = webdriver.Edge(service=service, options=options)

    try:
        driver.get("https://x.com.br/")

        username = wait_for_element(driver, By.ID, "username")
        username.click()
        username.send_keys("user")

        nxt = wait_for_element(driver, By.ID, "next")
        nxt.click()

        time.sleep(5)

    finally:
        driver.quit()
