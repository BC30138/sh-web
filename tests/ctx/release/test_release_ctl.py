"""Проверка контроллера релизов"""
from shweb.ctx.release.interfaces import ReleaseRepo

def test_calls_repo(mocker, release_controller_client):
    repo_mock = mocker.patch.object(
        ReleaseRepo,
        'get',
        return_value=None,
    )
    release_controller_client.get('test_release_id')
    repo_mock.assert_called_once_with('test_release_id')
