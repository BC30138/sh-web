"""Проверка основного хранилища"""
import pytest

from shweb.services.object_storage import object_storage_client
from shweb.services.object_storage import Error as ObjectStorageError


def test_happy_path():
    result = object_storage_client.get('releases/traces/info.json')

    assert result is not None
    assert isinstance(result, dict)


def test_not_found():
    with pytest.raises(ObjectStorageError) as exc:
        object_storage_client.get('not/found/path')
    assert str(exc.value) == 'Retrieve object not/found/path error'


def test_invalid_format():
    with pytest.raises(ObjectStorageError) as exc:
        object_storage_client.get('releases/traces/cover.jpg')
    assert str(exc.value) == 'Incorrect type of response data'
