"""Сервис для получения данных из Бэндкамп"""
from ast import literal_eval
import requests
from typing import Optional

from bs4 import BeautifulSoup


class BandcampError(Exception):
    pass


class BandcampAPI:
    def get_id(bandcamp_link: Optional[str] = None) -> str:
        if bandcamp_link is None:
            raise BandcampError(
                'One of bancamp_id or bandcamp_link should be stated at least'
            )
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
