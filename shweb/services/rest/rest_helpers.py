"""Утилиты для работы REST API"""
import functools
import os.path
from typing import List

from flask import _request_ctx_stack as stack

from shweb.ctx.index.ctl import IndexCtl
from shweb.ctx.index.repo import IndexRepo
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


def mobile_template(path_tree: List[str], template: str):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if mobile_checker():
                kwargs['template'] = os.path.join(*path_tree, 'mobile', template)
            else:
                kwargs['template'] = os.path.join(*path_tree, 'web', template)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def utility_processor():
    return dict(
        get_release_list=get_release_list
    )


def get_release_ctl() -> ReleaseCtl:
    return ReleaseCtl(
        repo=ReleaseRepo(),
        bandcamp_service=ReleaseBandcampRepo(),
    )


def get_index_ctl() -> IndexCtl:
    return IndexCtl(
        repo=IndexRepo(),
    )
