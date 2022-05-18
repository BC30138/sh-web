"""Сервис для получения данных из хранилища"""
from typing import Optional


class ObjectStorage:
    @classmethod
    def get(cls, path: str) -> Optional[dict]:
        NotImplementedError
