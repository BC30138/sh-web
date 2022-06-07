"""Контроллер для действий над индекс-страницой"""

import logging
from typing import List, Dict, IO

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

    def upload(
        self,
        index_entity: IndexEntity,
        to_delete: List[str],
        files: Dict[str, IO[bytes]],
    ):
        self._repo.upload(
            index_entity=index_entity,
            to_delete=to_delete,
            files=files,
        )
