"""Контроллер для действий над релизами"""
import abc
from typing import Optional

from shweb.ctx.release.model import ReleaseEntity
from shweb.ctx.release.repo import IReleaseRepo


class IReleaseCtl(abc.ABC):
    @abc.abstractmethod
    def get(self, release_id: str) -> Optional[ReleaseEntity]:
        raise NotImplementedError


class ReleaseCtl(IReleaseCtl):
    def __init__(self, repo: IReleaseRepo) -> None:
        self._repo = repo

    def get(self, release_id: str) -> Optional[ReleaseEntity]:
        return self._repo.get(release_id)
