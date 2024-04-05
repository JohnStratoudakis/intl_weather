from hamcrest import assert_that, equal_to
from pathlib import Path
import pytest

from datetime import datetime, timedelta, timezone
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
    cache_dir = Path(files(tests.data))

    # WHEN
    _weather = Weather(lat=lat, lon=lon, cache_dir=cache_dir)

    # THEN
    hourly = _weather.Hourly()
    t = datetime(2024, 4, 5, 12, 56, 5, 0, tzinfo=timezone.utc)
    assert_that(hourly.generatedAt(), equal_to(t))
    assert_that(hourly.get_num_periods(), equal_to(156))
    assert_that(hourly.get_period(idx=0).startTime(), equal_to(datetime(2024, 4, 5, 8, 0, 0, tzinfo=timezone(timedelta(hours=-4)))))
    assert_that(hourly.get_period(idx=0).endTime(), equal_to(datetime(2024, 4, 5, 9, 0, 0, tzinfo=timezone(timedelta(hours=-4)))))

    # Other fields of interest
    # "isDaytime": true,
    # "temperature": 41,
    # "temperatureUnit": "F",

    # "probabilityOfPrecipitation": {
    # "unitCode": "wmoUnit:percent",
    #    "value": 4
    #},
    #"relativeHumidity": {
    #    "unitCode": "wmoUnit:percent",
    #    "value": 70
    #},
    #"windSpeed": "14 mph",
    #"windDirection": "W",
    #"icon": "https://api.weather.gov/icons/land/day/bkn,4?size=small",
    #"shortForecast": "Partly Sunny",
