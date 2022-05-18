from flask import request, session
from flask_babel import _


from shweb.config import Config


def get_release_types():
    return {
        'Single': _('Single'),
        'Album': _('Album'),
        'Ep': _('Ep'),
        'single': _('single'),
        'album': _('album'),
        'ep': _('ep')
    }


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
