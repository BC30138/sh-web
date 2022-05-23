"""Сервис для получения данных из Бэндкамп"""
import logging
from ast import literal_eval
import requests

from bs4 import BeautifulSoup


class BandcampError(Exception):
    pass


class BandcampAPI:
    @classmethod
    def get_id(cls, bandcamp_link: str) -> str:
        try:
            response = requests.get(bandcamp_link)
        except requests.RequestException:
            logging.warning('Bad bandcamp link')
            raise BandcampError('Bad bandcamp link')

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            bandcamp_id = str(literal_eval(
                soup.head.find("meta", {"name": "bc-page-properties"})['content']
            )['item_id'])
            logging.info(f'fetched bandcamp id {bandcamp_id}')
            return bandcamp_id
        except ValueError:
            logging.warning('Bandcamp page error')
            raise BandcampError('Bandcamp page error')
