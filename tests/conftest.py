import pytest

from shweb.ctx.release.ctl import ReleaseCtl
from shweb.ctx.release.repo import ReleaseRepo


@pytest.fixture()
def release_controller_client():
    yield ReleaseCtl(
        repo=ReleaseRepo()
    )
