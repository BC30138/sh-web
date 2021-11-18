import requests
from flask_babel import _
from flask import current_app


def get_release_types():
    return {
        'Single': _('Single'),
        'Album': _('Album'),
        'Ep': _('Ep'),
        'single': _('single'),
        'album': _('album'),
        'ep': _('ep')
    }


def get_month_name():
    return {
        'jan': _('jan'),
        'feb': _('feb'),
        'mar': _('mar'),
        'apr': _('apr'),
        'may': _('may'),
        'jun': _('jun'),
        'jul': _('jul'),
        'aug': _('aug'),
        'sep': _('sep'),
        'oct': _('oct'),
        'nov': _('nov'),
        'dec': _('dec')
    }


def get_release_list():
    base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
    response = requests.get(f"{base}/releases/release-list.json")
    releases: list = response.json()['releases']
    releases = list(map(
        lambda x: x.update({'lang_type': get_release_types()[x['type']]}) or x,
        releases
    ))
    return releases
