"""Проверка рендера страницы индекса"""
from unittest.mock import PropertyMock

import pytest

from shweb.config import Config
from shweb.ctx.index.ctl import IndexCtl


@pytest.mark.parametrize('locale', ['ru', 'en'])
@pytest.mark.parametrize(
    'client_name, template',
    [
        ('web', 'public/web/index.html'),
        ('mobile', 'public/mobile/index.html')
    ]
)
def test_calls(
    mocker,
    parametrized_app,
    locale,
    client_name,
    template,
    index_factory,
    decoded_index_response_factory,
):
    app = parametrized_app[client_name]
    client = app.test_client()

    ctl_mock = mocker.patch.object(
        IndexCtl,
        'get',
        return_value=index_factory(),
    )
    mocker.patch.object(
        Config,
        'AWS_CLOUD_FRONT_DOMAIN',
        new_callable=PropertyMock,
        return_value='https/example.com',
    )
    render_mock = mocker.patch(
        'shweb.services.rest.routes.public.index.render_template',
        return_value='ok',
    )
    mocker.patch(
        'shweb.services.rest.schemas.index.get_locale',
        return_value=locale,
    )

    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'ok'

    ctl_mock.assert_called_once_with()
    index = decoded_index_response_factory(
        locale,
    )
    render_mock.assert_called_once_with(
        template,
        style_code=index[client_name]['style'],
        content_code=index[client_name]['content'],
    )
