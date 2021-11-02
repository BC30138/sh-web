import os

from flask import Flask, request, session
from flask_mobility import Mobility
from flask_babel import Babel

from shweb.utils import get_release_list

from shweb.routes import index, releases, feed
from shweb.routes import admin


app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

app.config['AWS_ACCESS_KEY'] = os.environ['AWS_ACCESS_KEY']
app.config['AWS_SECRET_KEY'] = os.environ['AWS_SECRET_KEY']
app.config['AWS_REGION'] = os.environ['AWS_REGION']

app.config['AWS_CLOUD_FRONT_DOMAIN'] = os.environ['AWS_CLOUD_FRONT_DOMAIN']

app.config['COGNITO_REGION'] = app.config['AWS_REGION']
app.config['COGNITO_USERPOOL_ID'] = os.environ['AWS_USER_POOL_ID']
app.config['COGNITO_APP_CLIENT_ID'] = os.environ['AWS_APP_CLIENT_ID']
app.config['COGNITO_APP_CLIENT_SECRET'] = os.environ['AWS_APP_CLIENT_SECRET']
app.config['COGNITO_JWKS_KEYS_URL'] = f"https://cognito-idp.{app.config['COGNITO_REGION']}.amazonaws.com/{app.config['COGNITO_USERPOOL_ID']}/.well-known/jwks.json"


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


@app.context_processor
def utility_processor():
    return dict(
        get_release_list=get_release_list
    )


app.register_blueprint(index.blueprint, url_prefix="/")
app.register_blueprint(releases.blueprint, url_prefix="/releases")
app.register_blueprint(feed.blueprint, url_prefix="/feed")
app.register_blueprint(admin.blueprint, url_prefix="/admin")
