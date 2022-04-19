#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from pathlib import Path
import os
import csv
import time

# config
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument("--disable-dev-shm-usage")
chromeOptions.add_argument("--no-sandbox")
# s=Service('/usr/bin/chromedriver') #Linux
s = Service('C:/chromedriver/chromedriver.exe')  # Windows
driver = webdriver.Chrome(service=s, options=chromeOptions)

# target
url = 'https://www.uniklinik-freiburg.de/karriere/stellenangebote.html'

# path to csv
datapath = 'data/ukf_car/'

# create path var
path = datapath + 'ukf_1.csv'


# lists
jobs = [
    'DATETIME',
    'Ärztlicher Dienst', 'Forschung/Wissenschaft',
    'Med.- techn. Dienst', 'Pflege- und Funktionsdienst',
    'Soziale pädagogische und therapeutische Berufe', 'Verwaltung / Management / IT',
    'Gewerbliche- und Service-Berufe', 'Minijobs / Aushilfen / student. Hilfskräfte',
    'Ausbildung / Praktikum / Freiwilligendienst', 'Sonstige'
]
quantity = []

# check csv sum
head_len = len(jobs)

# create timestamp
dateTimeObj = datetime.now()
dateObj = dateTimeObj.date()
timeObj = dateTimeObj.time()

dateStr = dateObj.strftime("%Y-%m-%d")
timeStr = timeObj.strftime("%H:%M")

timestamp = [dateStr + ' ' + timeStr]

print(timestamp)

Path(path).touch(exist_ok=True)  # if csv don't exists

# write zeros if file is empty
csv_empty = os.stat(path).st_size == 0

if csv_empty is True:
    with open(path, 'w', encoding='utf8', newline='') as f:
        writeZero = csv.writer(f)
        writeZero.writerow(jobs)


try:
    # scraper
    print('###### STARTING SCRIPT #######')
    driver.get(url)
    time.sleep(1)

    # search for quantity
    search2 = driver.find_elements(By.CLASS_NAME, "category-teaser-badge")

    for i in range(len(search2)-1):
        # print([search2[i].get_attribute('innerHTML')])
        quantity.append(search2[i].get_attribute('innerHTML'))

    driver.quit()
except Exception:
    print(timeStr + ' ' + dateStr + ': ' + "ERROR: URL MAY BE BROKEN")
    pass


# Write to DB
data = timestamp + quantity

time.sleep(0.5)

# check csv sum
data_len = len(data)

# write data into csv
if head_len == data_len:
    with open(path, 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        print(timeStr + ' ' + dateStr + ': Data collecting successful!')
else:
    print("ERROR! CSV HEADER NOT MATCHING DATA")

