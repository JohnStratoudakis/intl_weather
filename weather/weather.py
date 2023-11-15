
import json
from pathlib import Path
from typing import Optional


class Metadata:
    pass

class Weather:
    def __init__(self, lat: float, lon: float,
            cache_dir: Optional[Path] = None):
        self._lat = lat
        self._lon = lon
        if cache_dir is None:
            cache_dir = Path('.')
        else:
            cache_dir = cache_dir

        self._metadata = Metadata()

    def get_c_from_f(fahrenheit: float) -> float:
        return (fahrenheit - 32) * 5/9

    def load_metadata(self, record: bool=False, use_cache: bool=False) -> str:
        """
        Find the gridX and gridY values for the given latitude
        and longitude pair, optionally save the response
        """
        url = f'https://api.weather.gov/points/{self._lat},{self._lon}'

        found_in_cache = False
        if use_cache:
            data = Path(f'./cache/zone_{self._lat}_{self._lon}.json').read_text()
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
                Path(f'./cache/zone_{self._lat}_{self._lon}.json').write_text(data_tab)

        self._metadata.city = data['properties']['relativeLocation']['properties']['city']
        self._metadata.state = data['properties']['relativeLocation']['properties']['state']
        self._metadata.forecast_url = data['properties']['forecast']
        self._metadata.forecast_hourly = data['properties']['forecastHourly']
        self._metadata.forecast_griddata = data['properties']['forecastGridData']
        self._metadata.forecast_stations = data['properties']['observationStations']
        self._metadata.grid_x = data['properties']['gridX']
        self._metadata.grid_y = data['properties']['gridY']
        return data

    def get_hourly(self,
                   forecast_hourly: str,
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

