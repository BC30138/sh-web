"""Проверка контроллера релизов"""
import pytest

from shweb.ctx.release.repo import ReleaseRepo, ReleaseBandcampRepo
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
        ReleaseBandcampRepo,
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
    assert release == release_repo


def test_not_found(
    mocker,
    release_controller_client,
):
    mocker.patch.object(
        ReleaseRepo,
        'get',
        return_value=None,
    )

    release = release_controller_client.get('test_release_id')
    assert release is None
