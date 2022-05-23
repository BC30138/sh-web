"""Проверка Bandcamp API"""
import pytest

from shweb.services.bandcamp import BandcampAPI
from shweb.services.bandcamp import Error as BandcampError


def test_happy_path():
    bandcamp_id = BandcampAPI.get_id('https://stanethuzhe.bandcamp.com/album/-')
    assert bandcamp_id == '1328992434'


def test_bad_link():
    with pytest.raises(BandcampError) as exc:
        BandcampAPI.get_id('bad.link')
    assert str(exc.value) == 'Bad bandcamp link'


def test_wrong_link():
    with pytest.raises(BandcampError) as exc:
        BandcampAPI.get_id('https://youtube.com/')
    assert str(exc.value) == 'Bandcamp page error'
