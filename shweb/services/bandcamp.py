"""Сервис для получения данных из Бэндкамп"""
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
            raise BandcampError('Bad bandcamp link')

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            return str(literal_eval(
                soup.head.find("meta", {"name": "bc-page-properties"})['content']
            )['item_id'])
        except ValueError:
            raise BandcampError('Bandcamp page error')
