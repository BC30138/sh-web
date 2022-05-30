"""Сущности для взаимодействия с пользователями админки"""

import dataclasses
from typing import Optional

from shweb.util.enums import AuthStatus


@dataclasses.dataclass
class IdentityEntity:
    username: str
    password: str
    auth_status: AuthStatus
    token: Optional[str] = None
