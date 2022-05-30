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


@dataclasses.dataclass
class ServiceEntity:
    name: str
    link: str


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
