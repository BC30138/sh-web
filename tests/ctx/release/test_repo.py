"""Проверка репозиторий релизов"""
from unittest.mock import MagicMock, Mock

from shweb.services.object_storage import ObjectStorageAPI
from shweb.ctx.release.repo import ReleaseRepo
import shweb.util.dateutils


def test_calls_object_storage(  # happy path
    mocker,
    object_storage_response,
    release_factory
):
    storage_mock = mocker.patch.object(
        ObjectStorageAPI,
        'get',
        return_value=object_storage_response,
    )
    expected_release = release_factory()

    release = ReleaseRepo.get('test_release')
    storage_mock.assert_called_once_with('releases/test_release/info.json')
    assert release == expected_release


def test_not_found(
    mocker,
    object_storage_response,
):
    mocker.patch.object(
        ObjectStorageAPI,
        'get',
        return_value=None,
    )

    release = ReleaseRepo.get('test_release')
    assert release is None


def test_calls_date_util(
    mocker,
    object_storage_response,
    release_factory,
):
    mocker.patch.object(
        ObjectStorageAPI,
        'get',
        return_value=object_storage_response,
    )
    expected_release = release_factory()
    date_util_mock = mocker.patch.object(
        shweb.util.dateutils,
        'date_from_str',
        Mock(return_value=expected_release.release_date),
    )

    release = ReleaseRepo.get('test_release')
    date_util_mock.assert_called()
    assert release.release_date is not None
    assert release == expected_release
