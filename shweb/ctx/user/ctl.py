"""Контроллер для работы с пользователям"""

import abc
import logging

from shweb.ctx.index.model import IndexEntity
from shweb.ctx.index.adapter import IIndexRepo
from shweb.ctx.user.model import UserEntity


class IUserCtl(abc.ABC):
    @abc.abstractmethod
    def auth(self, user: UserEntity) -> IndexEntity:
        raise NotImplementedError


class UserCtl(IUserCtl):
    def __init__(
        self,
        repo: IIndexRepo,
    ) -> None:
        self._repo = repo

    def get(self) -> IndexEntity:
        logging.info('fetch index')
        return self._repo.get()
