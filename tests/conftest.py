import pytest

from shweb.ctx.release.ctl import ReleaseCtl
from shweb.ctx.release.interfaces import ReleaseRepo, ReleaseBandcampAPI


@pytest.fixture()
def release_controller_client():
    yield ReleaseCtl(
        repo=ReleaseRepo(),
        bandcamp_service=ReleaseBandcampAPI(),
    )
