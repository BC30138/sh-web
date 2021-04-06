from flask import Flask

from shweb.context import Environment as env
from shweb.routes import index


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.register_blueprint(index.blueprint, url_prefix="/")
