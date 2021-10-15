from flask import Flask, request, session
from flask_mobility import Mobility
from flask_babel import Babel, gettext
from flask_login import LoginManager

from shweb.context import Environment as env
from shweb.routes import index, releases, feed
from shweb.routes import admin

from warrant import Cognito

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

USER_POOL_ID = "eu-central-1_R7kMPFbB3"
CLIENT_ID = "35g94vf37ro8d2m8ab1nilld18"


@login_manager.request_loader
def load_user_from_request_header(request):
    try:
        access_token = request.headers["Authorization"]
        cognito = Cognito(USER_POOL_ID, CLIENT_ID, access_token)
        username = cognito.get_user()._metadata.get("username")
        if username is None:
            return None
        return "yeah"
    except Exception as e:
        return None


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
app.register_blueprint(admin.blueprint, url_prefix="/admin")
