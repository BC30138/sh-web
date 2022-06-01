"""Контроллер для действий над релизами"""

import logging
from typing import Optional

from shweb.ctx.release.model import ReleaseEntity, ReleaseListEntity
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
