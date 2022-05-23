"""Проверка репозиторий релизов"""
from shweb.services.object_storage import ObjectStorageAPI
from shweb.services.object_storage import Error as ObjectStrorageError
from shweb.services.bandcamp import BandcampAPI
from shweb.ctx.release.repo import ReleaseRepo, ReleaseBandcampRepo


# ------------ REPO TESTS --------------

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
        side_effect=ObjectStrorageError,
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
    date_util_mock = mocker.patch(
        'shweb.ctx.release.repo.date_from_str',
        return_value=expected_release.release_date,
    )

    release = ReleaseRepo.get('test_release')
    date_util_mock.assert_called_once_with('2022-05-19')
    assert release.release_date is not None
    assert release == expected_release

# -------- BANDCAMP REPO TESTS ---------


def test_calls_bandcamp_api(
    mocker,
):
    bandcamp_api_mock = mocker.patch.object(
        BandcampAPI,
        'get_id',
        return_value='test_id',
    )

    bandcamp_id = ReleaseBandcampRepo.get_id('https://test.com/test-id')

    bandcamp_api_mock.assert_called_once_with('https://test.com/test-id')
    assert bandcamp_id == 'test_id'
