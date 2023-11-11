#!/usr/bin/python3.11

from setuptools import setup

setup(
    name="IntlWeather",
    version="0.0.1",
    author="John Stratoudakis",
    author_email="johnstratoudakis@gmail.com",
    license="",
    packages=["weather"],
    entry_points={
        "console_scripts": [
            "intl_weather=Weather.__main__:main"
            ]
        },
)

