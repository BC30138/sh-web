"""Предстваления релизов."""

import dataclasses
from datetime import date
from typing import List, Optional

from shweb.util.enums import ReleaseType


@dataclasses.dataclass
class TrackEntity:
    name: str
    track_id: str
    written: Optional[str]
    lyrics: Optional[str]
    explicit: Optional[bool]

    @classmethod
    def from_dict(cls, track_dict: dict) -> 'TrackEntity':
        return cls(
            name=track_dict['name'],
            track_id=track_dict['track_id'],
            written=track_dict.get('written'),
            lyrics=track_dict.get('lyrics'),
            explicit=track_dict.get('explicit'),
        )


@dataclasses.dataclass
class ServiceEntity:
    name: str
    link: str

    @classmethod
    def from_dict(cls, service_dict: dict) -> 'ServiceEntity':
        return cls(
            name=service_dict['name'],
            link=service_dict['link'],
        )


@dataclasses.dataclass
class ReleaseEntity:
    release_id: str
    release_name: str
    release_type: ReleaseType
    services: List[ServiceEntity]
    tracklist: List[TrackEntity]
    bandcamp_id: Optional[str]
    bandcamp_link: Optional[str]
    release_date: Optional[date]
    default_open_text: Optional[str]
    youtube_videos: Optional[List[str]]

    @classmethod
    def from_dict(cls, release_dict: dict) -> 'ReleaseEntity':
        if release_dict.get('bandcamp_id') is None and release_dict.get('bandcamp_link') is None:
            raise ValueError('bandcamp_id or bandcamp_link must be specified')
        release_date = release_dict.get('release_date')
        return cls(
            release_id=release_dict['release_id'],
            release_name=release_dict['release_name'],
            release_type=ReleaseType(release_dict['release_type']),
            services=[ServiceEntity.from_dict(service) for service in release_dict['services']],
            tracklist=[TrackEntity.from_dict(track) for track in release_dict['tracklist']],
            bandcamp_id=release_dict.get('bandcamp_id'),
            bandcamp_link=release_dict.get('bandcamp_link'),
            release_date=None if release_date is None else date.fromisoformat(release_date),
            default_open_text=release_dict.get('default_open_text'),
            youtube_videos=release_dict.get('youtube_videos'),
        )


@dataclasses.dataclass
class ReleaseListItemEntity:
    release_id: str
    release_name: str
    release_type: ReleaseType


@dataclasses.dataclass
class ReleaseListEntity:
    releases: List[ReleaseListItemEntity]
