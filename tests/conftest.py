from datetime import date
from typing import Optional, Callable, List

import pytest

from shweb.ctx.release.ctl import ReleaseCtl
from shweb.ctx.release.interfaces import ReleaseRepo, ReleaseBandcampAPI
from shweb.ctx.release.model import ReleaseEntity, ServiceEntity, TrackEntity
from shweb.util.dateutils import date_from_str
from shweb.util.enums import ReleaseType


@pytest.fixture()
def release_controller_client() -> ReleaseCtl:
    yield ReleaseCtl(
        repo=ReleaseRepo(),
        bandcamp_service=ReleaseBandcampAPI(),
    )


@pytest.fixture()
def object_storage_response() -> dict:
    yield {
      "bandcamp_id": "1328992434",
      "bandcamp_link": "https://stanethuzhe.bandcamp.com/album/-",
      "date": "2021-12-13",
      "default_open_text": "",
      "release_id": "reki",
      "release_name": "реки",
      "services": [
        {
          "name": "apple",
          "link": "https://music.apple.com/us/album/%D1%80%D0%B5%D0%BA%D0%B8/1598527539"
        },
        {
          "name": "yandex",
          "link": "https://music.yandex.ru/album/19784610"
        },
      ],
      "tracklist": [
        {
          "lyrics": "текст песни",
          "name": "название трека",
          "explicit": False,
          "id": "test_track_id"
        },
        {
          "lyrics": "",
          "name": "название трека 2",
          "explicit": True,
          "id": "test_track_id_2",
        },
      ],
      "type": "Album",
      "youtube_videos": [
        "kC0YqmnbQJQ",
      ]
    }


@pytest.fixture
def service_factory() -> Callable[..., ServiceEntity]:
    def _make_service(
        name: str = "test_service",
        link: str = "https://test.link.com/test_track",
    ) -> ServiceEntity:
        return ServiceEntity(
            name=name,
            link=link,
        )

    yield _make_service


@pytest.fixture()
def release_type_fabric() -> Callable[..., ReleaseType]:
    def _make_release_type(release_type: Optional[str] = "Album") -> ReleaseType:
        return ReleaseType(release_type)
    yield _make_release_type


@pytest.fixture()
def track_fabric() -> Callable[..., TrackEntity]:
    def _make_track(
        name: Optional[str] = 'test_track',
        id: Optional[str] = 'test_track_id',
        written: Optional[str] = None,
        lyrics: Optional[str] = 'текст песни',
        explicit: Optional[bool] = False,
    ) -> TrackEntity:
        return TrackEntity(
            name=name,
            id=id,
            written=written,
            lyrics=lyrics,
            explicit=explicit
        )
    yield _make_track


@pytest.fixture()
def date_fabric() -> Callable[..., date]:
    def _make_date(
        test_date: Optional[str] = None,
    ) -> date:
        if test_date is not None:
            return date_from_str(test_date)
        return date.today()
    yield _make_date


@pytest.fixture()
def release_factory(
    object_storage_response,
    release_type_fabric,
    service_factory,
    track_fabric,
    date_fabric,
) -> Callable[..., ReleaseEntity]:
    def _make_release(
        release_id: Optional[str] = object_storage_response['release_id'],
        release_name: Optional[str] = object_storage_response['release_name'],
        release_type: Optional[ReleaseType] = None,
        services: Optional[List[ServiceEntity]] = None,
        tracklist: Optional[List[TrackEntity]] = None,
        bandcamp_id: Optional[str] = object_storage_response['bandcamp_id'],
        bandcamp_link: Optional[str] = object_storage_response['bandcamp_link'],
        release_date: Optional[date] = None,
        default_open_text: Optional[str] = None,
        youtube_videos: Optional[List[str]] = None,
    ) -> ReleaseEntity:
        if release_type is None:
            release_type = release_type_fabric(object_storage_response['type'])
        if services is None:
            services = [service_factory(**service) for service in object_storage_response['services']]
        if tracklist is None:
            tracklist = [track_fabric(**track) for track in object_storage_response['tracklist']]
        if release_date is None:
            release_date = date_fabric(object_storage_response['date'])
        return ReleaseEntity(
            release_id=release_id,
            release_name=release_name,
            type=release_type,
            services=services,
            tracklist=tracklist,
            bandcamp_id=bandcamp_id,
            bandcamp_link=bandcamp_link,
            date=release_date,
            default_open_text=default_open_text,
            youtube_videos=youtube_videos,
        )
    yield _make_release
