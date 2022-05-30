"""Контроллер для работы с пользователям"""

import abc
import logging
from typing import Optional

from shweb.ctx.identity.adapter import IIdentityAdapter
from shweb.ctx.identity.model import IdentityEntity


class IIdentityCtl(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, username: str, password: str) -> IdentityEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def forget_password(self, username) -> IdentityEntity:
        raise NotImplementedError


class IdentityCtl(IIdentityCtl):
    def __init__(
        self,
        identity_adapter: IIdentityAdapter,
    ) -> None:
        self._identity_adapter = identity_adapter

    def authenticate(self, username: Optional[str], password: Optional[str]) -> Optional[IdentityEntity]:
        if username and password:
            return self._identity_adapter.authenticate(username, password)
        return None

    def forget_password(self, username) -> IdentityEntity:
        return self._identity_adapter.forget_password(username) if username else None
