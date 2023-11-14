

class Weather:
    def __init__(self, lat: float, long: float):
        self._lat = lat
        self._long = long

    def get_c_from_f(fahrenheit: float) -> float:
        return (fahrenheit - 32) * 5/9

    def get_zone(self, record: bool=False, use_cache: bool=False) -> str:
        """
        Find the gridX and gridY values for the given latitude
        and longitude pair, optionally save the response
        """
        url = f'https://api.weather.gov/points/{self._lat},{self._long}'

        found_in_cache = False
        if use_cache:
            data = Path(f'./cache/zone_{self._lat}_{self._long}.json').read_text()
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
                Path(f'./cache/zone_{self._lat}_{self._long}.json').write_text(data_tab)

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

