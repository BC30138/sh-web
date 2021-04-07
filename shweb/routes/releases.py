import json

from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_mobility.decorators import mobile_template

blueprint = Blueprint("release-page", __name__)


def get_release_data(release, release_path, release_static_path):
    with open(f'{release_path}/info.json') as rf:
        release_info = json.load(rf)
    release_data = {
        'release-name': release_info['release-name'],
        'release-id': release,
        'date': release_info['date'],
        'default-open-text': release_info['default-open-text'],
        'bandcamp-id': release_info['bandcamp-id'],
        'bandcamp-link': release_info['bandcamp-id'],
        'services': release_info['services'],
        'cover': f"{release_static_path}/cover.jpg"
    }

    return release_data, release_info['tracklist']


@blueprint.route('/releases/<release>', methods=['GET', 'POST'])
@mobile_template('{mobile/}release.html')
def releases(release, template):
    release_static_path = f"/static/releases/{release}"
    release_path = f"shweb{release_static_path}"
    try:
        release_data, tracklist_info = get_release_data(
            release,
            release_path,
            release_static_path
        )
        tracklist = ''
        if request.method == "GET":
            track_id = request.args.get('trackid', "")
            if track_id == "" and release_data['default-open-text']:
                track_id = release_data['default-open-text']
            for id, track in enumerate(tracklist_info):
                if track['track-id'] == track_id:
                    with open(f"{release_path}/{track_id}.txt") as lyricf:
                        lyrics = lyricf.read()
                    tracklist += f"""
                    <button class="track-btn" type="submit" name="track-id" value="null" style="color:white;">
                        {id + 1}. {track['track-name']}
                    </button>
                    <pre><b>Written By:</b> {track['written-by']}</pre>
                    <pre>{lyrics}</pre>
                    """
                else:
                    tracklist += f"""
                    <button class="track-btn" type="submit" name="track-id" value="{track['track-id']}">
                        {id + 1}. {track['track-name']}
                    </button>
                    """
            return render_template(template, release_data=release_data, tracklist=tracklist)
        else:
            track_id = request.form.get('track-id', "")
            return redirect(url_for('.releases', release=release, trackid=track_id))
    except:
        abort(404)
