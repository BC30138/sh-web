from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template

from shweb.services.rest.rest_helpers import get_release_ctl
from shweb.services.rest.schemas.release import ReleaseScheme

blueprint = Blueprint("release-page", __name__)


@blueprint.route('/<release_id>', methods=['GET', 'POST'])
@mobile_template('{mobile/}release.html')
def releases(release_id, template):
    release_ctl = get_release_ctl()
    release = release_ctl.get(release_id)

    return render_template(
        template,
        release=ReleaseScheme.from_entity(release),
        bodyproperty=f'onload=openLyrics(\'{release.default_open_text}\')'
    )
