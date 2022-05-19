"""Сервис для получения данных из хранилища"""
from typing import Optional


class ObjectStorageAPI:
    @classmethod
    def get(cls, path: str) -> Optional[dict]:
        raise NotImplementedError
