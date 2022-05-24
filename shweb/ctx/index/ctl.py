"""Контроллер для действий над индекс-страницой"""

import abc
import logging

from shweb.ctx.index.model import IndexEntity
from shweb.ctx.index.repo import IIndexRepo


class IIndexCtl(abc.ABC):
    @abc.abstractmethod
    def get(self) -> IndexEntity:
        raise NotImplementedError


class IndexCtl(IIndexCtl):
    def __init__(
        self,
        repo: IIndexRepo,
    ) -> None:
        self._repo = repo

    def get(self) -> IndexEntity:
        logging.info('fetch index')
        return self._repo.get()
