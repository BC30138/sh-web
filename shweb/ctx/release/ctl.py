"""Контроллер для действий над релизами"""

import logging
from typing import Optional, IO

from shweb.ctx.release.model import ReleaseEntity, ReleaseListEntity, ReleaseListItemEntity
from shweb.ctx.release.repo import IReleaseRepo, IReleaseBandcampRepo


class Error(Exception):
    pass


class ReleaseCtl:
    def __init__(
        self,
        repo: IReleaseRepo,
        bandcamp_service: IReleaseBandcampRepo,
    ) -> None:
        self._repo = repo
        self._bandcamp_service = bandcamp_service

    def get(self, release_id: str) -> Optional[ReleaseEntity]:
        logging.info(f'fetch release {release_id}')
        release = self._repo.get(release_id)
        if release and release.bandcamp_id is None:
            if release.bandcamp_link is None:
                logging.warning('One of bandcamp_id or bandcamp_link should be stated at least')
                raise Error('One of bandcamp_id or bandcamp_link should be stated at least')
            release.bandcamp_id = self._bandcamp_service.get_id(release.bandcamp_link)
            if release.bandcamp_id is None:
                logging.warning(f'Bandcamp error for {release.bandcamp_link}')
                raise Error('Bandcamp error')
        logging.info(f'fetched release {release}')
        return release

    def get_list(self) -> ReleaseListEntity:
        logging.info('fetch release list')
        return self._repo.get_list()

    def change_order(self, releases_order: dict):
        # release_order '<order>': '<track_id>'
        # получаем текущий список релизов
        object_storage_release_list = self._repo.get_list()

        # создание по новому отсортированной сущности списка
        new_order_releases = []
        for key in sorted(releases_order):
            release = next(
                release for release in object_storage_release_list.releases
                if release.release_id == releases_order[key]
            )
            new_order_releases.append(release)
        new_order_release_list = ReleaseListEntity(releases=new_order_releases)

        # загрузка списка в хранилище
        self._repo.upload_list(new_order_release_list)

        return new_order_release_list

    def upload_release_objects(
        self,
        release_entity: ReleaseEntity,
        cover: Optional[IO[bytes]] = None,
        og: Optional[IO[bytes]] = None,
    ):
        self._repo.upsert_release_objects(
            release_entity=release_entity,
            cover=cover,
            og=og,
        )

    def upsert_release_list_item(
        self,
        new_release: ReleaseListItemEntity,
        release_id: Optional[str] = None,
    ) -> ReleaseListEntity:
        release_list_entity = self._repo.get_list()
        release_ids = [release.release_id for release in release_list_entity.releases]
        # new
        if release_id is None:
            if new_release.release_id in release_ids:
                raise Error('Release with this name already exists')
            release_list_entity.releases.append(new_release)
        # rename
        elif release_id != new_release.release_id:
            if new_release.release_id in release_ids:
                raise Error('Release with this name already exists')
            release_list_entity.releases = list(
                filter(lambda item: item.release_id != release_id, release_list_entity.releases)
            )
            self._repo.move_release_objects(release_id, new_release.release_id)
            release_list_entity.releases.append(new_release)
        # change data
        elif new_release.release_id in release_ids:
            for release in release_list_entity.releases:
                if release.release_id == new_release.release_id:
                    release.release_name = new_release.release_name
                    release.release_type = new_release.release_type
                    break

        self._repo.upload_list(release_list_entity)
        return release_list_entity

    def remove_release(self, release_id: str):
        self._repo.remove_release_objects(release_id)
        release_list_entity = self._repo.get_list()
        release_list_entity.releases = list(
            filter(lambda item: item.release_id != release_id, release_list_entity.releases)
        )
        self._repo.upload_list(release_list_entity)
