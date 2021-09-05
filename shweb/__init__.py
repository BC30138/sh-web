from flask import Flask
from flask_mobility import Mobility

from shweb.context import Environment as env
from shweb.routes import index, releases, feed


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Mobility(app)

app.register_blueprint(index.blueprint, url_prefix="/")
app.register_blueprint(releases.blueprint, url_prefix="/")
app.register_blueprint(feed.blueprint, url_prefix="/")
