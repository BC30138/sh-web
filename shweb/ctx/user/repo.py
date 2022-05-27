"""Адаптер для доступа к системе аутентификации"""

import abc


class IUserAdapter(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get(cls):
        raise NotImplementedError


class UserAdapter(IUserAdapter):
    @classmethod
    def get(cls):
        pass
