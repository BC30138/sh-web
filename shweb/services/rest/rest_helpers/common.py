import functools

from flask import session, url_for, Request
from jose import jwt
from werkzeug.utils import redirect
from marshmallow import EXCLUDE
from webargs.flaskparser import FlaskParser

from shweb.services.auth_service import auth_client
from shweb.services.rest.rest_helpers.getters import get_release_ctl
from shweb.services.rest.schemas.release import ReleaseListScheme
from shweb.util.enums import AuthStatus


def get_release_list():
    release_ctl = get_release_ctl()
    release_list_entity = release_ctl.get_list()
    return ReleaseListScheme.from_entity(release_list_entity)['releases']


def get_user_info_from_token():
    return jwt.get_unverified_claims(session['id_token'])


def utility_processor():
    return dict(
        get_release_list=get_release_list,
        get_user_info_from_token=get_user_info_from_token,
    )


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'id_token' in session:
            state = auth_client.check_id_token(session['id_token'])
            if state == AuthStatus.VALID:
                return func(*args, **kwargs)
            return redirect(url_for('admin.login', status=state.value))
        else:
            return redirect(url_for('admin.login'))
    return wrapper


class RequestParser(FlaskParser):
    DEFAULT_UNKNOWN_BY_LOCATION = {
        'query': EXCLUDE,
        'json': EXCLUDE,
        'form': EXCLUDE,
        'files': EXCLUDE,
    }



request_parser = RequestParser()


@request_parser.location_loader("request-files")
def load_data(request: Request, schema):
    return {'files': request.files.items()}
