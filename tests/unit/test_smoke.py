
#from weather.util import Util
#   ut = Util()
from pathlib import Path
from weather.weather import Weather
import tests.data
from importlib.resources import files

# import Weather Install intl_weather package
# Import Weather class
#  - Call get zone
#  - Call get hourly
#  - Return current Temp + location + Image
LAT_FLUSHING = "40.7607"
LON_FLUSHING = "-73.7873"

#cache_dir = 'tests/data'
def test_get_zone():
    # Types of queries:
    #  - Zone
    #  - Forecast
    #  - Hourly
    #  - Grid
    # GIVEN
    lat = LAT_FLUSHING
    lon = LON_FLUSHING
    print(f'{tests.data}')
    print(f'{files(tests.data)}')
    cache_dir = Path(files(tests.data))
    # WHEN
    _weather = Weather(lat=lat, lon=lon, cache_dir=cache_dir)
    _weather.load_metadata(use_cache=True)
