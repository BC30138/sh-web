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
    schema = ReleaseSchema()
    schema_deserial = schema.load(release_json)
    schema_serial = schema.dump(schema_deserial)

    bodyproperty = f'onload=openLyrics(\'{schema_serial["default_open_text"]}\')'
    return render_template(
        template,
        release=schema_serial,
        bodyproperty=bodyproperty
    )
