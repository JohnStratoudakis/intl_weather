
from datetime import datetime, timedelta, timezone
import json
import logging
from pathlib import Path
import requests
from typing import Optional


logger = logging.getLogger()


date_fmt = '%Y-%m-%dT%H:%M:%S%z'

class Metadata:
    pass

class Period:
    def __init__(self, in_json):
        self._in_json = in_json

    def startTime(self) -> datetime:
        date_str = self._in_json['startTime']
        return datetime.strptime(date_str, date_fmt)

    def endTime(self) -> datetime:
        date_str = self._in_json['endTime']
        return datetime.strptime(date_str, date_fmt)

class Hourly:
    def __init__(self, in_json):
        self._in_json = in_json

    def generatedAt(self) -> datetime:
        #"generatedAt": "2024-04-05T12:56:05+00:00",
        date_str = self._in_json['properties']['generatedAt']
        date_str = date_str[:-3] + date_str[-2:]

        gen_date = datetime.strptime(date_str, date_fmt)
        return gen_date

    def get_period(self, idx) -> Period:
        return Period(self._in_json['properties']['periods'][idx])

    def get_num_periods(self) -> int:
        return len(self._in_json['properties']['periods'])
class Weather:
    def __init__(self,
                 lat: float,
                 lon: float,
                 cache_dir: Optional[Path] = None,
                 use_cache: bool = False):
        self._lat = lat
        self._lon = lon
        if cache_dir is None:
            self._cache_dir = Path('.')
        else:
            self._cache_dir = cache_dir
        #print(f'self._cache_dir: {self._cache_dir}')

        self._metadata = Metadata()
        self._hourly = None
        self._hourly_data = None
        self._load_metadata(record=True, use_cache=use_cache)
        self._load_hourly(record=True)

    def _make_request_with_cache(self,
                                 url: str,
                                 cache_file: Path,
                                 record: bool = False) -> str:
        result_str = None
        print(f'Checking for cache file:\n  - {cache_file}')
        if cache_file.exists() is False:
            print(f'Cache file not found, making request')

            r = requests.get(url=url)
            # extracting data in json format
            data = r.json()
            if record:
                result_str = json.dumps(data, indent=4)
                if self._cache_dir.exists() is False:
                    self._cache_dir.mkdir()
                cache_file.write_text(result_str)
        else:
            print(f'Cache file found')
            result_str = cache_file.read_text()
            data = json.loads(result_str)

        return data

    def _get_c_from_f(fahrenheit: float) -> float:
        return (fahrenheit - 32) * 5/9

    def _load_metadata(self,
                       record: bool=False,
                       use_cache: bool=False) -> str:
        """
        Find the gridX and gridY values for the given latitude
        and longitude pair, optionally save the response
        """
        url = f'https://api.weather.gov/points/{self._lat},{self._lon}'

        zone_json_file = self._cache_dir.joinpath(f'zone_{self._lat}_{self._lon}.json')
        print(f'zone_json_file: {zone_json_file}')

        data = self._make_request_with_cache(url=url,
                                             cache_file=zone_json_file,
                                             record=record)

        self._metadata.city = data['properties']['relativeLocation']['properties']['city']
        self._metadata.state = data['properties']['relativeLocation']['properties']['state']
        self._metadata.forecast_url = data['properties']['forecast']
        self._metadata.forecast_hourly = data['properties']['forecastHourly']
        self._metadata.forecast_griddata = data['properties']['forecastGridData']
        self._metadata.forecast_stations = data['properties']['observationStations']
        self._metadata.grid_x = data['properties']['gridX']
        self._metadata.grid_y = data['properties']['gridY']

        return data

    def _load_hourly(self,
                     record: bool=False,
                     use_cache: bool=False) -> str:

        forecast_hourly_url = self._metadata.forecast_hourly
        grid_x = self._metadata.grid_x
        grid_y = self._metadata.grid_y
        hourly_cache_file = self._cache_dir.joinpath(f'hourly_{grid_x}_{grid_y}.json')

        data = self._make_request_with_cache(url=forecast_hourly_url,
                                             cache_file=hourly_cache_file,
                                             record=record)
        self._hourly_data = data
        self._hourly = Hourly(self._hourly_data)

    def Hourly(self) -> Hourly:
        return self._hourly
