"""Проверка контроллера релизов"""

import pytest

pytestmark = pytest.mark.asyncio

def test_calls_repo(release_controller_client):
    release_controller_client.get('traces')
