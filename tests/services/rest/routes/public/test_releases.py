"""Проверка REST API публичной страницы релиза"""
from unittest.mock import PropertyMock

import pytest
from flask import Request

from shweb.ctx.release.ctl import ReleaseCtl


def test_calls_controller(client, mocker, release_factory):
    repo_mock = mocker.patch.object(
        ReleaseCtl,
        'get',
        return_value=release_factory(),
    )
    response = client.get('/releases/test_id')
    assert response.status_code == 200

    repo_mock.assert_called_once_with('test_id')

@pytest.mark.parametrize(
    'client_name, template',
    [
        ('web', 'public/web/release.html'),
        ('mobile', 'public/mobile/release.html')
    ]
)
def test_calls_render(
    parametrized_client,
    client_name,
    mocker,
    release_factory,
    release_scheme,
    template,
):
    client = parametrized_client[client_name]
    release = release_factory()
    mocker.patch.object(
        ReleaseCtl,
        'get',
        return_value=release,
    )
    render_mock = mocker.patch(
        'shweb.services.rest.routes.public.releases.render_template',
        return_value='ok',
    )

    response = client.get(f'/releases/{release.release_id}')
    assert response.status_code == 200
    assert response.data == b'ok'

    render_mock.assert_called_once_with(
        template,
        release=release_scheme,
        bodyproperty=f'onload=openLyrics(\'{release.default_open_text}\')'
    )
