import os

from flask import Flask, request, session
from flask_mobility import Mobility
from flask_babel import Babel
from flask_cognito import CognitoAuth

# from warrant import Cognito

from shweb.utils import load_releases

from shweb.routes import index, releases, feed
from shweb.routes import admin


app = Flask(__name__)

app.config['AWS_ACCESS_KEY'] = os.environ['AWS_ACCESS_KEY']
app.config['AWS_SECRET_KEY'] = os.environ['AWS_SECRET_KEY']
app.config['AWS_REGION'] = os.environ['AWS_REGION']
app.config['COGNITO_REGION'] = app.config['AWS_REGION']
app.config['COGNITO_USERPOOL_ID'] = os.environ['AWS_USER_POOL_ID']
app.config['COGNITO_APP_CLIENT_ID'] = os.environ['AWS_APP_CLIENT_ID']
app.config['COGNITO_CHECK_TOKEN_EXPIRATION'] = True

cogauth = CognitoAuth(app)


@app.before_first_request
def startup_load():
    load_releases(app)


# @login_manager.request_loader
# def load_user_from_request_header(request):
#     try:
#         access_token = request.headers["Authorization"]
#         cognito = Cognito(USER_POOL_ID, CLIENT_ID, access_token)
#         username = cognito.get_user()._metadata.get("username")
#         if username is None:
#             return None
#         return "yeah"
#     except Exception as e:
#         return None


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
