#!/usr/bin/python3.11

import json

from pathlib import Path
import requests
from typing import Dict


def get_c_from_f(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5/9

def get_zone(lat: str, long: str, record: bool=False, use_cache: bool=False) -> str:
    """
    Find the gridX and gridY values for the given latitude
    and longitude pair, optionally save the response
    """
    url = f'https://api.weather.gov/points/{lat},{long}'

    found_in_cache = False
    if use_cache:
        data = Path(f'./cache/zone_{lat}_{long}.json').read_text()
        data = json.loads(data)
        found_in_cache = True
    if use_cache is False and found_in_cache is False:
        r = requests.get(url=url)

        # extracting data in json format
        data = r.json()
        data_tab = json.dumps(data, indent=4)

        if record:
            if Path('./cache').exists() is False:
                Path('./cache').mkdir()
            Path(f'./cache/zone_{lat}_{long}.json').write_text(data_tab)

    return data

def get_hourly(forecast_hourly: str,
               grid_x: str,
               grid_y: str,
               record: bool=False,
               use_cache: bool=False) -> str:
    r = requests.get(url=forecast_hourly)

    #if use_cache:
    #    data = Path(f'./cache/hourly_{
    # extracting data in json format
    data = r.json()
    data_tab = json.dumps(data, indent=4)
    if record:
        Path(f'./cache/hourly_{grid_x}_{grid_y}.json').write_text(data_tab)

    return data_tab


def lambda_handler(event, context):
    print(f'{event}')
    lat = event['latitude']
    long = event['longitude']

    #data = get_zone(lat, long, record=True)
    data = get_zone(lat, long, use_cache=True)

    city = data['properties']['relativeLocation']['properties']['city']
    state = data['properties']['relativeLocation']['properties']['state']
    forecast_url = data['properties']['forecast']
    forecast_hourly = data['properties']['forecastHourly']
    forecast_griddata = data['properties']['forecastGridData']
    forecast_stations = data['properties']['observationStations']
    grid_x = data['properties']['gridX']
    grid_y = data['properties']['gridY']
#"forecast": "https://api.weather.gov/gridpoints/OKX/40,38/forecast",
#"forecastHourly": "https://api.weather.gov/gridpoints/OKX/40,38/forecast/hourly",
#"forecastGridData": "https://api.weather.gov/gridpoints/OKX/40,38",
#"observationStations": "https://api.weather.gov/gridpoints/OKX/40,38/stations",

    hourly = get_hourly(forecast_hourly,
                        grid_x,
                        grid_y,
                        record=True)
    print(f'Hourly: {hourly}')

    return {
        'statusCode': 200,
        'body': json.dumps(f'City: {city}, State: {state}')
    }

def get_request(latitude: str, longitude: str) -> Dict:
    event_dict = {
        "latitude": latitude,
        "longitude": longitude
    }
    return event_dict

if __name__ == "__main__":
    print('Testing...')

    # Washington Monument
    req = get_request(latitude="38.8894", longitude="-77.0352")

    # Flushing, Queens
    req = get_request(latitude="40.7607", longitude="-73.7873")

    res = lambda_handler(req, None)
    print(f'res: {res}')

