"""Контроллер для действий над индекс-страницой"""

import logging

from shweb.ctx.index.model import IndexEntity
from shweb.ctx.index.adapter import IIndexRepo


class IndexCtl:
    def __init__(
        self,
        repo: IIndexRepo,
    ) -> None:
        self._repo = repo

    def get(self) -> IndexEntity:
        logging.info('fetch index')
        return self._repo.get()
