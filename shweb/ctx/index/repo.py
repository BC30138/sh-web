"""Адаптер хранилища индекс-страницы"""

import abc

from shweb.ctx.index.model import IndexEntity, ClientIndexEntity
from shweb.services.object_storage import ObjectStorageAPI


class IIndexRepo(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get(cls) -> IndexEntity:
        raise NotImplementedError


class IndexRepo(IIndexRepo):
    @classmethod
    def get(cls) -> IndexEntity:
        storage_index = ObjectStorageAPI.get('index/index.json')
        return IndexEntity(
            web=ClientIndexEntity(
                style=storage_index['web']['style'],
                content=storage_index['web']['content'],
            ),
            mobile=ClientIndexEntity(
                style=storage_index['mobile']['style'],
                content=storage_index['mobile']['content'],
            ),
            files_list=storage_index.get('files_list', [])
        )
