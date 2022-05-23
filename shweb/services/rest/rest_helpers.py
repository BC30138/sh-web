from flask import _request_ctx_stack as stack
from shweb.utils import get_release_list

from shweb.ctx.release.ctl import ReleaseCtl
from shweb.ctx.release.repo import ReleaseRepo, ReleaseBandcampRepo


def mobile_checker():
    ctx = stack.top
    is_mobile = False
    if ctx is not None and hasattr(ctx, "request"):
        request = ctx.request
        is_mobile = getattr(request, "MOBILE", False)
    return is_mobile


def utility_processor():
    return dict(
        get_release_list=get_release_list
    )


def get_release_ctl() -> ReleaseCtl:
    return ReleaseCtl(
        repo=ReleaseRepo(),
        bandcamp_service=ReleaseBandcampRepo(),
    )
