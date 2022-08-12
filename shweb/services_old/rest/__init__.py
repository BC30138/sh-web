"""Инициация rest"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_mobility import Mobility
from flask_babel import Babel
from flask_apispec import FlaskApiSpec

from shweb.config import Config
from shweb.extensions.rest.router import register_blueprints
from shweb.extensions.rest.errorhandlers import register_errorhandlers
from shweb.extensions.rest.rest_helpers.common import utility_processor, request_parser
from shweb.extensions.rest.rest_helpers.translate import get_locale


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.template_folder = Config.TEMPLATES_PATH
    app.static_folder = Config.STATIC_PATH
    app.config['APISPEC_WEBARGS_PARSER'] = request_parser
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
