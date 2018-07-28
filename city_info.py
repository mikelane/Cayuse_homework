#!/usr/bin/env python3
import argparse
import logging.config
import os
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s %(asctime)s %(module)s | %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': os.environ.get('LOGGING_LEVEL', 'INFO'),
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': os.environ.get('LOGGING_LEVEL', 'INFO'),
            'propagate': True
        },
    }
}

logging.config.dictConfig(LOGGING)


class CityNotFound(Exception):
    pass


class City:
    def __init__(self,
                 zipcode,
                 open_wx_api_key=os.environ['OPEN_WX_API_KEY'],
                 google_maps_api_key=os.environ['GOOGLE_MAPS_API_KEY']):
        self.zipcode = zipcode
        self.open_wx_api_key = open_wx_api_key
        self.google_maps_api_key = google_maps_api_key
        self.lat, self.lon, self.city_name, self.current_temp = self.__get_coords_name_and_temp()
        self.timezone = self.__get_timezone()
        self.elevation = self.__get_elevation()

    def __get_coords_name_and_temp(self):
        url = 'http://api.openweathermap.org/data/2.5/weather'
        payload = {
            'APPID': self.open_wx_api_key,
            'zip': f'{self.zipcode},us',
            'units': 'imperial'
        }

        response = requests.get(url=url, params=payload)
        if response.status_code != 200:
            logger.error('ERROR: ZIP not found')
            raise CityNotFound(f'ZIP-code {self.zipcode} is invalid')

        data = response.json()
        logger.debug(f'OpenWeatherMap response: {data}')

        lat = data['coord']['lat']
        lon = data['coord']['lon']
        city_name = data['name']
        current_temp = int(round(data['main']['temp'], 0))

        return lat, lon, city_name, current_temp

    def __get_timezone(self):
        url = 'https://maps.googleapis.com/maps/api/timezone/json'
        payload = {
            'key': self.google_maps_api_key,
            'location': f'{self.lat},{self.lon}',
            'timestamp': f'{int(datetime.now().timestamp())}'
        }
        response = requests.get(url=url, params=payload)
        if response.status_code != 200:
            raise CityNotFound(f'Something went wrong with Google. The response was {response}')

        data = response.json()

        logger.debug(f'Google timezone response: {data}')

        return data['timeZoneName']

    def __get_elevation(self):
        url = 'https://maps.googleapis.com/maps/api/elevation/json'
        payload = {
            'key': self.google_maps_api_key,
            'locations': f'{self.lat},{self.lon}'
        }
        response = requests.get(url=url, params=payload)
        if response.status_code != 200:
            raise CityNotFound(f'Something went wrong with Google. The response was {response}')

        data = response.json()

        logger.debug(f'Google elevation response: {data}')

        return int(data['results'][0]['elevation'])

    def __str__(self):
        return f'At the location {self.city_name}, ' \
               f'the temperature is {self.current_temp}, ' \
               f'the timezone is {self.timezone}, ' \
               f'and the elevation is {self.elevation}.'


def main():
    parser = argparse.ArgumentParser(description='Cayuse City Information')
    parser.add_argument('--zip',
                        metavar='ZIPCODE',
                        required=True,
                        help='The ZIP-code of the city you are interested in')
    cli_args = parser.parse_args()

    logger.debug(f"Google Maps API Key: {os.environ['GOOGLE_MAPS_API_KEY']}")
    logger.debug(f"Open Weather API Key: {os.environ['OPEN_WX_API_KEY']}")
    logger.debug(f'Got zipcode {cli_args.zip}')
    try:
        city = City(cli_args.zip)
    except CityNotFound as e:
        print(e)
    else:
        print(city)
