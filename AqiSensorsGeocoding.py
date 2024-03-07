import json
import requests
from requests.structures import CaseInsensitiveDict

addresses = json.load(open('AqiAddresses.json'))
coords_list = []
stations_code = [98497, 107293, 98494, 98485, 460336, 69364, 414133, 21373, 156526, 67897, 112273, 460762,
                 116353, 246697, 196504, 74863, 193501]
for item in addresses:
    addr = item.split(',')
    text = addr[0] + '%20' + addr[1]
    url = "https://api.geoapify.com/v1/geocode/search?text=" + str(text) + "&apiKey="

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    features = resp.json()['features']
    geometry = features[0]['geometry']
    coords_list.append({'lat': geometry['coordinates'][1], 'lng': geometry['coordinates'][0],
                        'station': stations_code[addresses.index(item)]})

filename = 'AqiCords.json'
with open(filename, "w", encoding="utf-8") as json_file:
    json.dump(coords_list, json_file, ensure_ascii=False, indent=4)
