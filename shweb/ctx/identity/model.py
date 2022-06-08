"""Сущности для взаимодействия с пользователями админки"""

import dataclasses
from typing import Optional

from shweb.util.enums import AuthStatus


@dataclasses.dataclass
class IdentityEntity:
    username: str
    auth_status: AuthStatus
    password: Optional[str] = None
    token: Optional[str] = None
