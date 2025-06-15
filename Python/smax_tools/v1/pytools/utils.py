import csv
import re
import unicodedata
import time
import subprocess

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_column_values(file_path, column_index):
    values = []
    seen_rows = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            row_tuple = tuple(row[2:-2])
            if row_tuple not in seen_rows:
                seen_rows.add(row_tuple)
                values.append(row[column_index].strip('\"'))
    return values

def get_column_values1(file_path, column_index):
    values = []
    seen_rows = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            row_tuple = tuple(row[1:])
            if row_tuple not in seen_rows:
                seen_rows.add(row_tuple)
                values.append(row[column_index].strip('\"').strip())
    return values

def transform_text(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = text.replace('ç', 'c').replace('Ç', 'C')
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)

    stopwords = {'de', 'e', 'a', 'o', 'as', 'os', 'da', 'do', 'das', 'dos', 'em', 'um', 'uma'}

    words = text.split()
    words = [word for word in words if word.lower() not in stopwords]
    text = ''.join(word.capitalize() for word in words)

    if text and not text[0].isalpha():
        text = 'A' + text

    return text

def press_tab(driver, times=1):
    for _ in range(times):
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(1)

def press_enter(driver):
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
    time.sleep(1)

def is_boolean_list(items):
    normalized_items = [unicodedata.normalize('NFKD', item).encode('ASCII', 'ignore').decode('ASCII').lower() for item in items]
    return set(normalized_items) == {'sim', 'nao'}

def login(driver, url, username, email, password):
    driver.get(url)
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(5)
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'i0116'))
    )
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)
    time.sleep(5)
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'i0118'))
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(40)

def kill_edge_processes():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao encerrar processos do Edge: {e}")