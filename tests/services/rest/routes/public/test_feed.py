"""Проверка рендера страницы новостей"""
import pytest


@pytest.mark.parametrize(
    'client_name, template',
    [
        ('web', 'public/web/feed.html'),
        ('mobile', 'public/mobile/feed.html')
    ]
)
def test_calls_render(
    parametrized_client,
    client_name,
    mocker,
    template,
):
    client = parametrized_client[client_name]
    render_mock = mocker.patch(
        'shweb.services.rest.routes.public.feed.render_template',
        return_value='ok',
    )

    response = client.get(f'/feed/')
    assert response.status_code == 200
    assert response.data == b'ok'

    render_mock.assert_called_once_with(template)
