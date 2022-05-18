"""Сервис для получения данных из хранилища"""
from typing import Optional


class ObjectStorage:
    @classmethod
    def get(path: str) -> Optional[dict]:
        NotImplementedError
