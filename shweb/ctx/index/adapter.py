"""Адаптер хранилища индекс-страницы"""

import abc
from typing import List, Dict, IO

from shweb.ctx.index.model import IndexEntity, ClientIndexEntity
from shweb.services.object_storage import object_storage_client


class IIndexRepo(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get(cls) -> IndexEntity:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def upload(
        cls,
        index_entity: IndexEntity,
        to_delete: List[str],
        files: Dict[str, IO[bytes]]
    ):
        raise NotImplementedError


class IndexRepo(IIndexRepo):
    index_path = 'index'
    index_files_path = 'index/files'

    @classmethod
    def get(cls) -> IndexEntity:
        storage_index = object_storage_client.get('index/index.json')
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

    @classmethod
    def upload(
        cls,
        index_entity: IndexEntity,
        to_delete: List[str],
        files: Dict[str, IO[bytes]]
    ):
        for filename, file in files:
            object_storage_client.upload_file(
                file=file,
                file_path=f'{cls.index_files_path}/{filename}'
            )

        object_storage_client.upload_json(
            json_data=index_entity.to_dict(),
            file_path=f'{cls.index_path}/index.json',
        )

        for item_to_delete in to_delete:
            object_storage_client.delete(
                prefix=f'{cls.index_files_path}/{item_to_delete}'
            )

        object_storage_client.create_invalidation(
            items=[f'/{cls.index_path}/*']
        )
