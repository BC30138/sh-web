"""Интерфейс хранилища релизов"""
import abc
from typing import Optional

from shweb.ctx.release.model import ReleaseEntity, ServiceEntity, TrackEntity
from shweb.services.object_storage import ObjectStorageAPI
from shweb.services.bandcamp import BandcampAPI
from shweb.util.enums import ReleaseType
from shweb.util.dateutils import date_from_str


class IReleaseRepo(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get(cls, release_id: str) -> Optional[ReleaseEntity]:
        raise NotImplementedError


class ReleaseRepo(IReleaseRepo):
    @classmethod
    def get(cls, release_id: str) -> Optional[ReleaseEntity]:
        storage_release = ObjectStorageAPI.get(f'releases/{release_id}/info.json')
        return ReleaseEntity(
            release_id=storage_release['release_id'],
            release_name=storage_release['release_name'],
            type=ReleaseType(storage_release['type']),
            services=[ServiceEntity(
                name=service['str'],
                link=service['link'],
            ) for service in storage_release['services']],
            tracklist=[TrackEntity(
                name=track['name'],
                id=track['id'],
                written=track.get('written'),
                lyrics=track.get('lyrics'),
                explicit=track.get('explicit'),
            ) for track in storage_release['tracklist']],
            bandcamp_id=storage_release.get('bandcamp_id'),
            bandcamp_link=storage_release.get('bandcamp_link'),
            date=date_from_str(
                storage_release['date']
            ) if 'date' in storage_release else None,
            default_open_text=storage_release.get('default_open_text'),
            youtube_videos=storage_release.get('youtube_videos'),
        ) if storage_release is not None else None


class IReleaseBandcampAPI(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_id(cls, bandcamp_link: str) -> str:
        raise NotImplementedError


class ReleaseBandcampAPI(IReleaseBandcampAPI):
    @classmethod
    def get_id(cls, bandcamp_link: str) -> str:
        return BandcampAPI.get_id(bandcamp_link)
