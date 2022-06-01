"""Интерфейс хранилища релизов"""
import abc
import logging
from typing import Optional

from shweb.ctx.release.model import ReleaseEntity, ServiceEntity, TrackEntity, ReleaseListEntity, ReleaseListItemEntity
from shweb.util.enums import ReleaseType
from shweb.services.object_storage import object_storage_client
from shweb.services.object_storage import Error as ObjectStorageError
from shweb.services.bandcamp import bandcamp_client
from shweb.services.bandcamp import Error as BandcampError
from shweb.util.dateutils import date_from_str


class IReleaseRepo(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get(cls, release_id: str) -> Optional[ReleaseEntity]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_list(cls) -> ReleaseListEntity:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def upload_list(cls, release_list_entity: ReleaseListEntity):
        raise NotImplementedError


class ReleaseRepo(IReleaseRepo):
    @classmethod
    def get(cls, release_id: str) -> Optional[ReleaseEntity]:
        try:
            storage_release = object_storage_client.get(f'releases/{release_id}/info.json')
        except ObjectStorageError as exc:
            logging.warning(f'object not found {exc}')
            return None
        logging.info(f'fetched release from storage {storage_release}')
        storage_release['services'] = [
            ServiceEntity(
                name=service['name'],
                link=service['link'],
            ) for service in storage_release['services']
        ]
        storage_release['type'] = ReleaseType(storage_release['type'])
        storage_release['tracklist'] = [
            TrackEntity(
                name=track['name'],
                track_id=track['id'],
                written=track.get('written'),
                lyrics=track.get('lyrics'),
                explicit=track.get('explicit'),
            ) for track in storage_release['tracklist']
        ]
        storage_release['date'] = date_from_str(
            storage_release['date']
        ) if 'date' in storage_release else None
        return ReleaseEntity(
            release_id=storage_release['release_id'],
            release_name=storage_release['release_name'],
            release_type=storage_release['type'],
            services=storage_release['services'],
            tracklist=storage_release['tracklist'],
            bandcamp_id=storage_release.get('bandcamp_id'),
            bandcamp_link=storage_release.get('bandcamp_link'),
            release_date=storage_release.get('date'),
            default_open_text=storage_release.get('default_open_text'),
            youtube_videos=storage_release.get('youtube_videos'),
        )

    @classmethod
    def get_list(cls) -> ReleaseListEntity:
        try:
            storage_release_list = object_storage_client.get(f'releases/release-list.json')
        except ObjectStorageError as exc:
            logging.warning(f'object not found {exc}')
            raise FileNotFoundError

        releases = []
        for release_raw in storage_release_list['releases']:
            releases.append(ReleaseListItemEntity(
                release_id=release_raw['id'],
                release_name=release_raw['name'],
                release_type=ReleaseType(release_raw['type'].capitalize())
            ))

        return ReleaseListEntity(releases=releases)

    @classmethod
    def upload_list(cls, release_list_entity: ReleaseListEntity):
        release_list_fp = 'releases/release-list.json'
        object_storage_client.upload_json(
            json_data={
                'releases': [dict(
                    id=release.release_id,
                    type=release.release_type.value,
                    name=release.release_name,
                ) for release in release_list_entity.releases]
            },
            file_path=release_list_fp,
        )
        object_storage_client.create_invalidation(["/" + release_list_fp])


class IReleaseBandcampRepo(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_id(cls, bandcamp_link: str) -> Optional[str]:
        raise NotImplementedError


class ReleaseBandcampRepo(IReleaseBandcampRepo):
    @classmethod
    def get_id(cls, bandcamp_link: str) -> Optional[str]:
        try:
            return bandcamp_client.get_id(bandcamp_link)
        except BandcampError as exc:
            logging.warning(exc)
            return None
