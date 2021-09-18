from flask import Flask, request, session
from flask_mobility import Mobility
from flask_babel import Babel, gettext

from shweb.context import Environment as env
from shweb.routes import index, releases, feed


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = {
    'en': "English",
    'ru': "Russian"
}
Mobility(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    if not session.get('lang_code', None):
        if request.args.get('lang'):
            session.lang_code = request.args.get('lang')
            session.lang_arg = f"?lang={session.lang_code}"
        else:
            session.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
            session.lang_arg = ""
    return session.lang_code


app.register_blueprint(index.blueprint, url_prefix="/")
app.register_blueprint(releases.blueprint, url_prefix="/releases")
app.register_blueprint(feed.blueprint, url_prefix="/feed")
