# pip install selenium webdriver-manager psutil

import os
import json
import psutil

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def close_edge_instances():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'msedge' in proc.info['name'].lower():
            proc.kill()

def setup_driver():
    edge_options = Options()
    edge_options.add_argument("user-data-dir=C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Edge\\User Data")
    edge_options.add_argument("profile-directory=Default")
    edge_options.add_argument("--start-maximized")
    service = Service(executable_path="C:\\edgedriver_win64\\msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver

def access_initial_page(driver):
    driver.get("https://csc.cemig.com.br/saw/Requests")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def fetch_json(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
    json_text = driver.find_element(By.TAG_NAME, "pre").text
    return json.loads(json_text)

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    close_edge_instances()
    driver = setup_driver()
    access_initial_page(driver)
    url = "https://x/rest/766894589/ems/Request?filter=(Active+%3D+%27true%27+and+AssignedToGroup+%3D+%27198286%27)&layout=Id,DisplayLabel,Description,RegisteredForServiceComponent,AssignedToPerson,PhaseId,ProcessId,SLT.SLATargetDate,SLT.OLATargetDate,RegisteredForServiceComponent.DisplayLabel,RegisteredForServiceComponent.SubType,RegisteredForServiceComponent.IsDeleted,AssignedToPerson.Name,AssignedToPerson.Avatar,AssignedToPerson.Location,AssignedToPerson.IsVIP,AssignedToPerson.OrganizationalGroup,AssignedToPerson.Upn,AssignedToPerson.IsDeleted&meta=totalCount&order=AssignedToPerson.Name+desc,AssignedToPerson.Location+desc,AssignedToPerson.IsVIP+desc,AssignedToPerson.OrganizationalGroup+desc,AssignedToPerson.Upn+desc&size=250&skip=0"
    data = fetch_json(driver, url)
    save_json(data, "response.json")
    driver.quit()

main()
