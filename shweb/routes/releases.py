import json

from flask import Blueprint, render_template, abort
from flask_mobility.decorators import mobile_template

blueprint = Blueprint("release-page", __name__)


def get_release_data(release, release_path, release_static_path):
    with open(f'{release_path}/info.json') as rf:
        release_info: dict = json.load(rf)
    release_data = {
        'release-name': release_info['release-name'],
        'release-id': release,
        'date': release_info['date'],
        'bandcamp-id': release_info['bandcamp-id'],
        'bandcamp-link': release_info['bandcamp-id'],
        'services': release_info['services'],
        'cover': f"{release_static_path}/cover.jpg",
        'type': release_info['type'],
        'youtube-videos': release_info.get("youtube-videos", [])
    }

    tracklist = []

    for track in release_info['tracklist']:
        with open(f"{release_path}/{track['id']}.txt") as lyricf:
            track['lyrics'] = lyricf.read()
        tracklist.append(track)

    return release_data, release_info['tracklist'], release_info['default-open-text']


@ blueprint.route('/releases/<release>', methods=['GET', 'POST'])
@ mobile_template('{mobile/}release.html')
def releases(release, template):
    release_static_path = f"/static/releases/{release}"
    release_path = f"shweb{release_static_path}"
    release_data, tracklist, open_lyrics = get_release_data(
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
