"""Тесты утилит времени"""
from datetime import date
from shweb.util.dateutils import date_from_str

def test_date_happy_path():
    assert date(year=2022, month=1, day=27) == date_from_str('2022-01-27')
