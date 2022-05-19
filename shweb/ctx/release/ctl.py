"""Контроллер для действий над релизами"""
import abc
from typing import Optional

from shweb.ctx.release.model import ReleaseEntity
from shweb.ctx.release.repo import IReleaseRepo, IReleaseBandcampAPI


class Error(Exception):
    pass


class IReleaseCtl(abc.ABC):
    @abc.abstractmethod
    def get(self, release_id: str) -> Optional[ReleaseEntity]:
        raise NotImplementedError


class ReleaseCtl(IReleaseCtl):
    def __init__(
        self,
        repo: IReleaseRepo,
        bandcamp_service: IReleaseBandcampAPI,
    ) -> None:
        self._repo = repo
        self._bandcamp_service = bandcamp_service

    def get(self, release_id: str) -> Optional[ReleaseEntity]:
        release = self._repo.get(release_id)
        if release and release.bandcamp_id is None:
            if release.bandcamp_link is None:
                raise Error('One of bandcamp_id or bandcamp_link should be stated at least')
            release.bandcamp_id = self._bandcamp_service.get_id(release.bandcamp_link)
        return release
