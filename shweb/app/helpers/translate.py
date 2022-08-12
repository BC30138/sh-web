from flask import request, session

from shweb.config import Config


def get_locale():
    if not session.get('lang_code', None):
        if request.args.get('lang'):
            session.lang_code = request.args.get('lang')
            session.lang_arg = f"?lang={session.lang_code}"
        else:
            session.lang_code = request.accept_languages.best_match(Config.LANGUAGES)
            session.lang_arg = ""
    return session.lang_code
