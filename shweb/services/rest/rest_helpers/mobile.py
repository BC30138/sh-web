"""REST утилиты для работы с мобильными запросами"""

import os
import functools
from typing import List, Optional

from flask import _request_ctx_stack as stack


def mobile_checker():
    ctx = stack.top
    is_mobile = False
    if ctx is not None and hasattr(ctx, "request"):
        request = ctx.request
        is_mobile = getattr(request, "MOBILE", False)
    return is_mobile


def mobile_template(
    path_tree:
    List[str],
    template: str,
    include_is_mobile: Optional[bool] = False,
):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            is_mobile = mobile_checker()
            if is_mobile:
                kwargs['template'] = os.path.join(*path_tree, 'mobile', template)
            else:
                kwargs['template'] = os.path.join(*path_tree, 'web', template)
            if include_is_mobile:
                kwargs['is_mobile'] = is_mobile
            return f(*args, **kwargs)
        return wrapper
    return decorator
