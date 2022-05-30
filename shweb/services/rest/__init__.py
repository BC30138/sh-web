"""Инициация rest"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_mobility import Mobility
from flask_babel import Babel

from shweb.config import Config
from shweb.services.rest.translate_helpers import get_locale
from shweb.services.rest.router import register_blueprints
from shweb.services.rest.errorhandlers import register_errorhandlers
from shweb.services.rest.rest_helpers.common import utility_processor


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.template_folder = Config.TEMPLATES_PATH
    app.static_folder = Config.STATIC_PATH
    CORS(app)
    Mobility(app)
    babel = Babel(app)
    babel.locale_selector_func = get_locale

    @app.route('/health')
    def health():
        return jsonify({"status": "ok"}), 200

    register_blueprints(app)
    register_errorhandlers(app)

    app.template_context_processors[None].append(utility_processor)
    return app
