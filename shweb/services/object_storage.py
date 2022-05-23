"""Сервис для получения данных из хранилища"""
import requests
import json

from typing import Optional
from shweb.config import Config


class Error(Exception):
    pass


class NotFound(Error):
    pass


class ObjectStorageAPI:
    @classmethod
    def get(
        cls,
        path: str,
        cloud_front_base: Optional[str] = Config.AWS_CLOUD_FRONT_DOMAIN,
    ) -> Optional[dict]:
        response = requests.get(f"{cloud_front_base}/{path}")
        if response.status_code == 404:
            raise NotFound(f'Object "{path}" not found')
        elif response.status_code != 200:
            raise Error(f'Retrive object {path} error')

        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            raise Error('Incorrect type of response data')
