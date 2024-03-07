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
    station_card = soup.find(id="station-card")

    aqi_header = station_card.find(class_="station-header")
    aqi_table_row = aqi_header.find_all('td', attrs={'style': 'pointer-events: none; font-size: 280%; line-height: 1; '
                                                          'text-align: center;'})

    if len(aqi_table_row) == 0:
        aqi = 'no data'

    else:
        aqi_table_row = aqi_table_row[0]
        aqi = aqi_table_row.text.strip()

    aqi_level_td = aqi_header.find_all('td', attrs={'style': 'pointer-events: none;'})

    if len(aqi_level_td) == 0:
        aqi_level = 'no data'
    else:
        aqi_level_td = aqi_level_td[0]
        aqi_level = aqi_level_td.find('div').text.strip()

    pollution_table = station_card.find(class_="station-table-species")
    pollution_rows = pollution_table.find_all('tr')
    pollutant = []
    for element in pollution_rows:
        pol_value = element.find(class_="station-specie-aqi")
        if pol_value is not None:
            pollutant.append(pol_value.text.strip())
    if len(pollutant) == 7:
        station_data = {'station id': stationId, 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'aqi': aqi,
                        'aqi_level': aqi_level, 'pm 2.5': pollutant[0], 'pm 10': pollutant[1],
                        'pm 1': pollutant[2], 'temp': pollutant[3], 'r.h': pollutant[4], 'pressure': pollutant[5],
                        'wind': pollutant[6]}
    elif len(pollutant) == 5:
        station_data = {'station id': stationId, 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'aqi': aqi,
                        'aqi_level': aqi_level, 'pm 2.5': pollutant[0], 'pm 10': pollutant[1],
                        'temp': pollutant[2], 'r.h': pollutant[3],
                        'wind': pollutant[4]}
    else:
        station_data = {'station id': stationId, 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'aqi': aqi,
                        'aqi_level': aqi_level, 'pm 2.5': pollutant[0], 'pm 10': pollutant[1],
                        'temp': pollutant[2], 'r.h': pollutant[3], 'pressure': pollutant[4],
                        'wind': pollutant[5]}
    return station_data


stations_code = [98497, 107293, 98494, 98485, 460336, 69364, 414133, 21373, 156526, 67897, 112273, 460762,
                 116353, 246697, 196504, 74863, 193501]
while True:
    for code in stations_code:
        row = stationScraper(code)
        filename = "dati vecchi/AqiData.json"
        file_path = Path(filename)
        if file_path.exists():
            with open(file_path) as fp:
                listObj = json.load(fp)
            listObj.append(row)
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(listObj, json_file, ensure_ascii=False, indent=4)
        else:
            listObj = [row]
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(listObj, json_file, ensure_ascii=False, indent=4)
    print('Aqi data retrieved ', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    time.sleep(3600)
