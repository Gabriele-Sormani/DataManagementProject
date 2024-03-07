import openmeteo_requests
import json
import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://air-quality-api.open-meteo.com/v1/air-quality"

data_list = []
coords = json.load(open('AqiCords.json'))
for cord in coords:
    params = {
        "latitude": cord['lat'],
        "longitude": cord['lng'],
        "hourly": ["us_aqi", "us_aqi_pm2_5", "us_aqi_pm10",
                   "us_aqi_nitrogen_dioxide", "us_aqi_carbon_monoxide", "us_aqi_ozone", "us_aqi_sulphur_dioxide"],
        "timezone": "Europe/Berlin",
        "start_date": "2024-02-03",
        "end_date": "2024-02-13"
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_us_aqi = hourly.Variables(0).ValuesAsNumpy()
    hourly_us_aqi_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
    hourly_us_aqi_pm10 = hourly.Variables(2).ValuesAsNumpy()
    hourly_us_aqi_nitrogen_dioxide = hourly.Variables(3).ValuesAsNumpy()
    hourly_us_aqi_carbon_monoxide = hourly.Variables(4).ValuesAsNumpy()
    hourly_us_aqi_ozone = hourly.Variables(5).ValuesAsNumpy()
    hourly_us_aqi_sulphur_dioxide = hourly.Variables(6).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s"),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
        "us_aqi": hourly_us_aqi, "us_aqi_pm2_5": hourly_us_aqi_pm2_5, "us_aqi_pm10": hourly_us_aqi_pm10,
        "us_aqi_nitrogen_dioxide": hourly_us_aqi_nitrogen_dioxide,
        "us_aqi_carbon_monoxide": hourly_us_aqi_carbon_monoxide, "us_aqi_ozone": hourly_us_aqi_ozone,
        "us_aqi_sulphur_dioxide": hourly_us_aqi_sulphur_dioxide}

    data_list.append((hourly_data, cord['station']))

hourly_df = pd.DataFrame()
for d in data_list:
    temp = pd.DataFrame(data=d[0])
    temp['station'] = d[1]
    hourly_df = pd.concat([hourly_df, temp], ignore_index=True)
hourly_df['datetime'] = hourly_df['date'].apply(lambda x: str(x))
hourly_df = hourly_df.drop('date', axis=1)
aqiData = hourly_df.to_dict('records')

filename = 'AqiOpenMeteoData.json'
with open(filename, "w", encoding="utf-8") as json_file:
    json.dump(aqiData, json_file, ensure_ascii=False, indent=4)
print('Aqi data retrived from OpenMeteoAPI')
