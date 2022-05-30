"""Контроллер для работы с пользователям"""

import abc
from typing import Optional

from shweb.ctx.identity.adapter import IIdentityAdapter
from shweb.ctx.identity.model import IdentityEntity


class IIdentityCtl(abc.ABC):
    @abc.abstractmethod
    def authenticate(
        self,
        username: Optional[str],
        password: Optional[str],
    ) -> Optional[IdentityEntity]:
        raise NotImplementedError

    @abc.abstractmethod
    def forget_password(
        self,
        username: Optional[str],
    ) -> Optional[IdentityEntity]:
        raise NotImplementedError

    @abc.abstractmethod
    def confirm_forgot_password(
        self,
        username: Optional[str],
        code: Optional[str],
        password: Optional[str],
    ) -> Optional[IdentityEntity]:
        raise NotImplementedError

    @abc.abstractmethod
    def change_password(
        self,
        username: Optional[str],
        password: Optional[str],
        cur_password: Optional[str],
    ) -> Optional[IdentityEntity]:
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

    def forget_password(self, username: Optional[str]) -> Optional[IdentityEntity]:
        return self._identity_adapter.forget_password(username) if username else None

    def confirm_forgot_password(
        self,
        username: Optional[str],
        confirmation_code: Optional[str],
        new_password: Optional[str],
    ) -> Optional[IdentityEntity]:
        if username and confirmation_code and new_password:
            return self._identity_adapter.confirm_forgot_password(
                username=username,
                confirmation_code=confirmation_code,
                new_password=new_password,
            )
        return None

    def change_password(
        self,
        username: Optional[str],
        password: Optional[str],
        new_password: Optional[str],
    ) -> Optional[IdentityEntity]:
        if username and password and new_password:
            return self._identity_adapter.change_password(
                username=username,
                password=password,
                new_password=new_password,
            )
        return None
