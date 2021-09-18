import json

from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template

from shweb.utils import get_release_types, get_month_name

blueprint = Blueprint("release-page", __name__)


def get_release_data(release, release_path, release_static_path):
    with open(f'{release_path}/info.json') as rf:
        release_info: dict = json.load(rf)
    release_data = {
        'release-name': release_info['release-name'],
        'release-id': release,
        'bandcamp-id': release_info['bandcamp-id'],
        'bandcamp-link': release_info['bandcamp-id'],
        'services': release_info['services'],
        'cover': f"{release_static_path}/cover.jpg",
        'youtube-videos': release_info.get("youtube-videos", [])
    }

    date_month = release_info['date'].split()[1]
    release_data['date'] = release_info['date'].replace(date_month, get_month_name()[date_month])
    release_data['type'] = get_release_types()[release_info['type']]

    tracklist = []

    for track in release_info['tracklist']:
        with open(f"{release_path}/{track['id']}.txt") as lyricf:
            track['lyrics'] = lyricf.read()
        tracklist.append(track)

    return release_data, release_info['tracklist'], \
        release_info['default-open-text'], release_info['type']


@ blueprint.route('/<release>', methods=['GET', 'POST'])
@ mobile_template('{mobile/}release.html')
def releases(release, template):
    release_static_path = f"/static/releases/{release}"
    release_path = f"shweb{release_static_path}"
    release_data, tracklist, open_lyrics, release_type = get_release_data(
        release,
        release_path,
        release_static_path
    )

    bodyproperty = f'onload=openLyrics(\'{open_lyrics}\')'
    return render_template(
        template,
        release_data=release_data,
        tracklist=tracklist,
        bodyproperty=bodyproperty
    )
