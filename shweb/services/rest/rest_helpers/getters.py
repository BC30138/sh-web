"""Гэттеры для получения контроллеров"""
from shweb.ctx.identity.adapter import IdentityAdapter
from shweb.ctx.index.adapter import IndexRepo
from shweb.ctx.index.ctl import IndexCtl
from shweb.ctx.release.ctl import ReleaseCtl
from shweb.ctx.identity.ctl import IdentityCtl
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


def get_identity_ctl() -> IdentityCtl:
    return IdentityCtl(
        identity_adapter=IdentityAdapter(),
    )
