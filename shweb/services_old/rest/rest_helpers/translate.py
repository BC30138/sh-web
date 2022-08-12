from flask import request, session
from flask_babel import _


from shweb.config import Config
from shweb.util.enums import ReleaseType


def compile_release_type(release_type: ReleaseType, is_upper=True) -> str:
    if release_type == ReleaseType.SINGLE:
        return _('Single') if is_upper else _('single')
    elif release_type == ReleaseType.ALBUM:
        return _('Album') if is_upper else _('album')
    elif release_type == ReleaseType.EP:
        return 'EP'
    else:
        raise ValueError('There is no such release type')


def get_month_names():
    return [
        _('jan'),
        _('feb'),
        _('mar'),
        _('apr'),
        _('may'),
        _('jun'),
        _('jul'),
        _('aug'),
        _('sep'),
        _('oct'),
        _('nov'),
        _('dec')
    ]


def get_locale():
    if not session.get('lang_code', None):
        if request.args.get('lang'):
            session.lang_code = request.args.get('lang')
            session.lang_arg = f"?lang={session.lang_code}"
        else:
            session.lang_code = request.accept_languages.best_match(Config.LANGUAGES)
            session.lang_arg = ""
    return session.lang_code
