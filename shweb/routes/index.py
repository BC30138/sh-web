# type: ignore
import requests
from flask import Blueprint, render_template, current_app, jsonify
from flask_mobility.decorators import mobile_template

from shweb.schemas.index_code import IndexCode
from shweb.services.rest.rest_helpers import mobile_checker

blueprint = Blueprint("index-page", __name__)


@blueprint.route('/')
@blueprint.route('/index')
@mobile_template('{mobile/}index.html')
def index(template):
    base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
    index_json = requests.get(f"{base}/index/index.json").json()

    index_schema = IndexCode()
    index_code_deserial = index_schema.load(index_json)
    index_code = index_schema.dump(index_code_deserial)

    if mobile_checker():
        device_code = index_code['mobile']
    else:
        device_code = index_code['web']

    style_code = device_code['style']
    content_code = device_code['content']
    return render_template(
        template, title='Home',
        style_code=style_code, content_code=content_code
    )


@blueprint.route('/health')
def health():
    return jsonify({"status": "ok"}), 200
