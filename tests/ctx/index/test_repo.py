"""Проверка репозитория индекса"""
import pytest

from shweb.ctx.index.adapter import IndexRepo
from shweb.services.object_storage import ObjectStorageAPI
from shweb.services.object_storage import Error as ObjectStorageError


def test_calls_object_storage(
    mocker,
    index_response,
    index_factory,
):
    storage_mock = mocker.patch.object(
        ObjectStorageAPI,
        'get',
        return_value=index_response,
    )
    expected_index = index_factory()

    release = IndexRepo.get()
    storage_mock.assert_called_once_with('index/index.json')
    assert release == expected_index


def test_not_found(
    mocker,
    object_storage_response,
):
    mocker.patch.object(
        ObjectStorageAPI,
        'get',
        side_effect=ObjectStorageError('Retrieve object index/index.json error'),
    )

    with pytest.raises(ObjectStorageError, match='Retrieve object index/index.json error'):
        IndexRepo.get()
