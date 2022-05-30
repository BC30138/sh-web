"""Сервис для получения данных из хранилища"""
import logging

import requests
import json

from shweb.config import Config


class Error(Exception):
    pass


class ObjectStorageAPI:
    def __init__(self, cloud_front_base: str):
        self._cloud_front_base = cloud_front_base

    def get(
        self,
        path: str,
    ) -> dict:
        response = requests.get(f"{self._cloud_front_base}/{path}")
        logging.info(f'GET {response.url} {response.status_code}')
        if response.status_code != 200:
            logging.warning(f'Retrieve object {path} error')
            raise Error(f'Retrieve object {path} error')

        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            logging.warning('Incorrect type of response data')
            raise Error('Incorrect type of response data')


object_storage_client = ObjectStorageAPI(Config.AWS_CLOUD_FRONT_DOMAIN)
