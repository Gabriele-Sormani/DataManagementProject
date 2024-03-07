import requests
import time
import json
from pathlib import Path
from datetime import datetime

south = 45.37084859807814
west = 8.992419551259218
north = 45.599188166161866
east = 9.361570914112974
api_key = ''
url = (f"https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=bbox:{west},{south},{east},{north}"
       f"&functionalClasses=1,2,3,4,5&apiKey={api_key}")
file_num = 11

while True:
    res = requests.get(url)

    if res.status_code == 200:
        response = res.json()
        filename = "NewTrafficData" + str(file_num) + ".json"
        file_path = Path(filename)
        if file_path.exists():
            with open(file_path) as fp:
                listObj = json.load(fp)
            listObj.append(response)
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(listObj, json_file, ensure_ascii=False, indent=4)
        else:
            listObj = [response]
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(listObj, json_file, ensure_ascii=False, indent=4)
        print('Traffic data retrieved ', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        file_size = file_path.stat().st_size
        if file_size > 1000000000:
            file_num += 1
            print('Changed file due to dimension too big', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    else:
        print('ERROR: ', res.json())

    time.sleep(3600)
