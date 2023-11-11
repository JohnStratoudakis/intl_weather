

import json

# importing the requests library
import requests

def lambda_handler(event, context):
    lat = event['latitude']
    long = event['longitude']
    url = f'https://api.weather.gov/points/{lat},{long}'

    r = requests.get(url=url)

    # extracting data in json format
    data = r.json()
    data_tab = json.dumps(data, indent=4)
    print(f'data: {data_tab}')

    city = data['properties']['relativeLocation']['properties']['city']
    state = data['properties']['relativeLocation']['properties']['state']
    return {
        'statusCode': 200,
        'body': json.dumps(f'City: {city}, State: {state}!')
    }

lat = "38.8894"
long = "-77.0352"
event_dict = {
        "latitude": lat,
        "longitude": long
}
