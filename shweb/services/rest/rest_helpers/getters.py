from shweb.ctx.index.adapter import IndexRepo
from shweb.ctx.index.ctl import IndexCtl
from shweb.ctx.release.ctl import ReleaseCtl
from shweb.ctx.release.repo import ReleaseRepo, ReleaseBandcampRepo


def get_release_ctl() -> ReleaseCtl:
    return ReleaseCtl(
        repo=ReleaseRepo(),
        bandcamp_service=ReleaseBandcampRepo(),
    )


def get_index_ctl() -> IndexCtl:
    return IndexCtl(
        repo=IndexRepo(),
    )
