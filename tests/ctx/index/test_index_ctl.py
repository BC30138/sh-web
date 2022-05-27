"""Проверка контроллера индекса"""

from shweb.ctx.index.repo import IndexRepo


def test_calls_repo(
    mocker,
    index_controller,
):
    repo_mock = mocker.patch.object(
        IndexRepo,
        'get',
        return_value=None,
    )
    index_controller.get()
    repo_mock.assert_called_once_with()


def test_happy_path(
    mocker,
    index_controller,
    index_factory,
):
    index_repo = index_factory()
    mocker.patch.object(
        IndexRepo,
        'get',
        return_value=index_repo,
    )

    index = index_controller.get()
    assert index == index_repo
