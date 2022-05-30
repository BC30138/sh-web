from datetime import date
from typing import Optional, Callable, List

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask import _request_ctx_stack as stack

from shweb.ctx.index.ctl import IndexCtl
from shweb.ctx.index.model import ClientIndexEntity, IndexEntity
from shweb.ctx.index.adapter import IndexRepo
from shweb.ctx.release.ctl import ReleaseCtl
from shweb.ctx.release.repo import ReleaseRepo, ReleaseBandcampRepo
from shweb.ctx.release.model import ReleaseEntity, ServiceEntity, TrackEntity, ReleaseType
from shweb.services.rest import create_app
from shweb.util.dateutils import date_from_str


@pytest.fixture()
def app() -> Flask:
    app = create_app()
    app.config.update({
        'TESTING': True,
    })
    return app


@pytest.fixture()
def mobile_app() -> Flask:
    app = create_app()
    app.config.update({
        'TESTING': True,
    })

    @app.before_request
    def before_request():
        ctx = stack.top
        ctx.request.MOBILE = True

    return app


@pytest.fixture()
def client(app) -> FlaskClient:
    yield app.test_client()


@pytest.fixture()
def mobile_client(mobile_app) -> FlaskClient:
    yield mobile_app.test_client()


@pytest.fixture()
def parametrized_client(client, mobile_client):
    return {
        'web': client,
        'mobile': mobile_client,
    }


@pytest.fixture()
def parametrized_app(app, mobile_app):
    return {
        'web': app,
        'mobile': mobile_app,
    }


@pytest.fixture()
def release_controller() -> ReleaseCtl:
    yield ReleaseCtl(
        repo=ReleaseRepo(),
        bandcamp_service=ReleaseBandcampRepo(),
    )


@pytest.fixture()
def index_controller() -> IndexCtl:
    yield IndexCtl(repo=IndexRepo())


@pytest.fixture()
def object_storage_response() -> dict:
    yield {
        'bandcamp_id': '1328992434',
        'bandcamp_link': 'https://stanethuzhe.bandcamp.com/album/-',
        'date': '2022-05-19',
        'default_open_text': 'test_track_id',
        'release_id': 'test_release_id',
        'release_name': 'тест',
        'services': [
          {
              'name': 'apple',
              'link': 'https://music.apple.com/us/album/%D1%80%D0%B5%D0%BA%D0%B8/1598527539'
          },
            {
              'name': 'yandex',
              'link': 'https://music.yandex.ru/album/19784610'
          },
        ],
        'tracklist': [
            {
                'lyrics': 'текст песни',
                'name': 'название трека',
                'explicit': False,
                'id': 'test_track_id'
            },
            {
                'lyrics': '',
                'name': 'название трека 2',
                'explicit': True,
                'id': 'test_track_id_2',
            },
        ],
        'type': 'Album',
        'youtube_videos': [
            'kC0YqmnbQJQ',
        ]
    }


@pytest.fixture()
def index_response() -> dict:
    style_base = 'test_style'
    content_base = 'lang is {{ lang_arg }}\nimage is {{ image=cover.jpg }}\ntranslated word: {{ translate={"en":"test","ru":"тест"} }}'
    return {
        'web': {
            'style': f'style for web\n{style_base}',
            'content': f'content for web\n{content_base}',
        },
        'mobile': {
            'style': f'style for mobile\n{style_base}',
            'content': f'content for mobile\n{content_base}',
        },
        'files_list': ['cover.jpg']
    }


@pytest.fixture()
def decoded_index_response_factory(
    index_response,
) -> Callable[..., dict]:
    def _make_decoded_index(
        locale: Optional[str] = 'en',
        cloud_base_url: Optional[str] = 'https/example.com',
    ) -> dict:
        if locale == 'ru':
            translated_word = 'тест'
        else:
            translated_word = 'test'
        content_base = f'lang is ?lang={locale}\nimage is {cloud_base_url}/index/files/cover.jpg\ntranslated word: {translated_word}'
        index_response['web']['style'] = f'<style>{index_response["web"]["style"]}</style>'
        index_response['web']['content'] = f'content for web\n{content_base}'
        index_response['mobile']['style'] = f'<style>{index_response["mobile"]["style"]}</style>'
        index_response['mobile']['content'] = f'content for mobile\n{content_base}'
        return index_response

    return _make_decoded_index


@pytest.fixture()
def release_scheme(object_storage_response):
    yield {
        'bandcamp_id': f'album={object_storage_response["bandcamp_id"]}',
        'bandcamp_link': object_storage_response['bandcamp_link'],
        'default_open_text': object_storage_response['default_open_text'],
        'release_date': '19 may 2022',
        'release_id': object_storage_response['release_id'],
        'release_name': object_storage_response['release_name'],
        'release_type': object_storage_response['type'],
        'services': object_storage_response['services'],
        'tracklist': [dict(
            written=track.get('written'),
            explicit=track.get('explicit'),
            lyrics=track.get('lyrics'),
            name=track.get('name'),
            track_id=track.get('id'),
        ) for track in object_storage_response['tracklist']],
        'youtube_videos': object_storage_response['youtube_videos']
     }


@pytest.fixture
def service_factory() -> Callable[..., ServiceEntity]:
    def _make_service(
        name: str = 'test_service',
        link: str = 'https://test.link.com/test_track',
    ) -> ServiceEntity:
        return ServiceEntity(
            name=name,
            link=link,
        )

    yield _make_service


@pytest.fixture()
def release_type_factory() -> Callable[..., ReleaseType]:
    def _make_release_type(release_type: Optional[str] = 'Album') -> ReleaseType:
        return ReleaseType(release_type)
    yield _make_release_type


@pytest.fixture()
def track_factory() -> Callable[..., TrackEntity]:
    def _make_track(
        name: Optional[str] = 'test_track',
        track_id: Optional[str] = 'test_track_id',
        written: Optional[str] = None,
        lyrics: Optional[str] = 'текст песни',
        explicit: Optional[bool] = False,
    ) -> TrackEntity:
        return TrackEntity(
            name=name,
            track_id=track_id,
            written=written,
            lyrics=lyrics,
            explicit=explicit
        )
    yield _make_track


@pytest.fixture()
def date_factory() -> Callable[..., date]:
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
    release_type_factory,
    service_factory,
    track_factory,
    date_factory,
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
        default_open_text: Optional[str] = object_storage_response['default_open_text'],
        youtube_videos: Optional[List[str]] = object_storage_response['youtube_videos'],
    ) -> ReleaseEntity:
        if release_type is None:
            release_type = release_type_factory(object_storage_response['type'])
        if services is None:
            services = [service_factory(**service) for service in object_storage_response['services']]
        if tracklist is None:
            tracklist = [
                track_factory(
                    name=track['name'],
                    track_id=track['id'],
                    written=track.get('written'),
                    lyrics=track.get('lyrics'),
                    explicit=track.get('explicit'),
                ) for track in object_storage_response['tracklist']
            ]
        if release_date is None:
            release_date = date_factory(object_storage_response['date'])
        return ReleaseEntity(
            release_id=release_id,
            release_name=release_name,
            release_type=release_type,
            services=services,
            tracklist=tracklist,
            bandcamp_id=bandcamp_id,
            bandcamp_link=bandcamp_link,
            release_date=release_date,
            default_open_text=default_open_text,
            youtube_videos=youtube_videos,
        )
    yield _make_release


@pytest.fixture()
def client_index_factory(
    index_response,
) -> Callable[..., ClientIndexEntity]:
    def _make_client_index(
        style: Optional[str] = index_response['web']['style'],
        content: Optional[str] = index_response['web']['content'],
    ) -> ClientIndexEntity:
        return ClientIndexEntity(
            style=style,
            content=content,
        )

    yield _make_client_index


@pytest.fixture()
def index_factory(
    index_response,
    client_index_factory,
) -> Callable[..., IndexEntity]:
    def _make_index(
        web: Optional[ClientIndexEntity] = None,
        mobile: Optional[ClientIndexEntity] = None,
        files_list: Optional[List[str]] = None,
    ) -> IndexEntity:
        if web is None:
            web = client_index_factory(**index_response['web'])
        if mobile is None:
            mobile = client_index_factory(**index_response['mobile'])
        if files_list is None:
            files_list = index_response['files_list']
        return IndexEntity(
            web=web,
            mobile=mobile,
            files_list=files_list,
        )

    yield _make_index
