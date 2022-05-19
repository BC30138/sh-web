"""Проверка контроллера релизов"""
import pytest

from shweb.ctx.release.repo import ReleaseRepo, ReleaseBandcampAPI
from shweb.ctx.release.ctl import Error as ReleaseError


def test_calls_repo(
    mocker,
    release_controller_client,
):
    repo_mock = mocker.patch.object(
        ReleaseRepo,
        'get',
        return_value=None,
    )
    release_controller_client.get('test_release_id')
    repo_mock.assert_called_once_with('test_release_id')


def test_calls_bandcamp_api(
    mocker,
    release_controller_client,
    release_factory,
):
    repo_release = release_factory(bandcamp_id=None)
    mocker.patch.object(
        ReleaseRepo,
        'get',
        return_value=repo_release,
    )
    bandcamp_mock = mocker.patch.object(
        ReleaseBandcampAPI,
        'get_id',
        return_value='test_id',
    )
    release = release_controller_client.get('test_release_id')
    bandcamp_mock.assert_called_once_with(repo_release.bandcamp_link)
    assert release.bandcamp_id == 'test_id'


def test_bandcamp_info_error(
    mocker,
    release_controller_client,
    release_factory,
):
    release_repo = release_factory(
        bandcamp_id=None,
        bandcamp_link=None,
    )
    mocker.patch.object(
        ReleaseRepo,
        'get',
        return_value=release_repo,
    )
    with pytest.raises(ReleaseError) as err:
        release_controller_client.get('test_release_id')

    assert str(err.value) == 'One of bandcamp_id or bandcamp_link should be stated at least'


def test_happy_path(
    mocker,
    release_controller_client,
    release_factory,
):
    release_repo = release_factory()
    mocker.patch.object(
        ReleaseRepo,
        'get',
        return_value=release_repo,
    )

    release = release_controller_client.get('test_release_id')
    assert release.release_id == release_repo.release_id
    assert release.release_name == release_repo.release_name
    assert release.bandcamp_id == release_repo.bandcamp_id
    assert release.bandcamp_link == release_repo.bandcamp_link
    assert release.type == release_repo.type
    assert release.default_open_text == release_repo.default_open_text
    assert release.tracklist == release_repo.tracklist
    assert release.services == release_repo.services
    assert release.youtube_videos == release_repo.youtube_videos
