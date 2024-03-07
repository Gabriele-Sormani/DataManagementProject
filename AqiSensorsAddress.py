import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pathlib import Path
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


def stationScraper(stationId):
    url = 'https://aqicn.org/station/@' + str(stationId)
    driver.get(url)

    try:
        jobs = WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'station-specie-aqi'))
        )

    except TimeoutError:
        print('Timeout error for AIQ data ', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        return {'msg': 'error timeout'}

    webpage = driver.page_source

    soup = BeautifulSoup(webpage, "html.parser")
    header = soup.find(id="h1header1")
    station_addr = header.text.strip()

    return station_addr


stations_code = [98497, 107293, 98494, 98485, 460336, 69364, 414133, 21373, 156526, 67897, 112273, 460762,
                 116353, 246697, 196504, 74863, 193501]
address_list = []
for code in stations_code:
    address = stationScraper(code)
    address_list.append(address)

filename = 'AqiAddresses.json'
with open(filename, "w", encoding="utf-8") as json_file:
    json.dump(address_list, json_file, ensure_ascii=False, indent=4)
