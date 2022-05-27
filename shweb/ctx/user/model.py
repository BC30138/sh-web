"""Сущности для взаимодействия с пользователями админки"""

import dataclasses
from typing import Optional


@dataclasses.dataclass
class UserEntity:
    username: str
    password: Optional[str]

