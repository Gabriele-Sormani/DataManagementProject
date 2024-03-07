from meteostat import Point, Hourly
from datetime import datetime
import json
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

start = datetime(2024, 2, 3)
end = datetime(2024, 2, 13)

stations_code = [98497, 107293, 98494, 98485, 460336, 69364, 414133, 21373, 156526, 67897, 112273, 460762,
                 116353, 246697, 196504, 74863, 193501]
coords = json.load(open('AqiCords.json'))
for cord in coords:
    index = coords.index(cord)
    milan = Point(cord['lat'], cord['lng'])

    data = Hourly(milan, start, end)

    res = data.fetch()
    res['datetime'] = pd.to_datetime(res.index, format='%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    res['station'] = stations_code[index]
    json_res = res.to_json(orient="index")
    parsed = json.loads(json_res)

    filename = 'MeteoData' + str(stations_code[index]) + '.json'

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(parsed, json_file, ensure_ascii=False, indent=4)
