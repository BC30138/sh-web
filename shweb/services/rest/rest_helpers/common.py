import functools

from flask import session, url_for
from jose import jwt
from werkzeug.utils import redirect
from marshmallow import EXCLUDE
from webargs.flaskparser import FlaskParser

from shweb.services.auth_service import auth_client
from shweb.util.enums import AuthStatus
from shweb.utils import get_release_list


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
    }


request_parser = RequestParser()
