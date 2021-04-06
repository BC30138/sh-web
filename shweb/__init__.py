from flask import Flask

from shweb.context import Environment as env
from shweb.routes import index


app = Flask(__name__)

app.register_blueprint(index.blueprint, url_prefix="/")
