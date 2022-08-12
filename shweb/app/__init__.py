from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api
from flask_mobility import Mobility
from flask_babel import Babel

from shweb.extensions.backend import register_blueprints as register_backend_blueprints
from shweb.app.helpers.translate import get_locale
from shweb.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.template_folder = Config.TEMPLATES_PATH
    app.static_folder = Config.STATIC_PATH
    CORS(app)
    Mobility(app)
    api = Api(app)
    babel = Babel(app)
    babel.locale_selector_func = get_locale

    @app.route('/health')
    def health():
        return jsonify({"status": "ok"}), 200

    register_backend_blueprints(api)

    return app