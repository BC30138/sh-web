import json
import requests

from flask import Blueprint, render_template, current_app
from flask_mobility.decorators import mobile_template

from shweb.schemas.release import ReleaseSchema

blueprint = Blueprint("release-page", __name__)


@ blueprint.route('/<release>', methods=['GET', 'POST'])
@ mobile_template('{mobile/}release.html')
def releases(release, template):
    base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
    release_json: dict = requests.get(f"{base}/releases/{release}/info.json").json()
    release_obj = ReleaseSchema().load(release_json)

    bodyproperty = f'onload=openLyrics(\'{release_obj["default_open_text"]}\')'
    return render_template(
        template,
        release=release_obj,
        bodyproperty=bodyproperty
    )
