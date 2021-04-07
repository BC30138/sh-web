import json

from flask import Blueprint, render_template, abort

blueprint = Blueprint("release-page", __name__)


@blueprint.route('/releases/<release>')
def releases(release):
    try:
        with open(f'shweb/static/releases/{release}/info.json') as rf:
            release_info = json.load(rf)
    except:
        abort(404)

    return release_info
    # return render_template("index.html", title='Home')
