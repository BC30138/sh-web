"""Сервис для получения данных из хранилища"""
import logging

import requests
import json

from typing import Optional
from shweb.config import Config


class Error(Exception):
    pass


class ObjectStorageAPI:
    @classmethod
    def get(
        cls,
        path: str,
        cloud_front_base: Optional[str] = Config.AWS_CLOUD_FRONT_DOMAIN,
    ) -> Optional[dict]:
        response = requests.get(f"{cloud_front_base}/{path}")
        logging.info(f'GET {response.url} {response.status_code}')
        if response.status_code != 200:
            logging.warning(f'Retrieve object {path} error')
            raise Error(f'Retrieve object {path} error')

        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            logging.warning('Incorrect type of response data')
            raise Error('Incorrect type of response data')
