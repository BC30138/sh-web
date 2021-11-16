import requests
from functools import wraps
from datetime import datetime
from enum import Enum


from flask import session, redirect, url_for, current_app
from jose import jwt, jwk
from jose.utils import base64url_decode


class TokenCheckState(Enum):
    VALID = 1
    INVALID = 2
    EXPIRED = 3
    INVALID_AUD = 4


def get_keys():
    response = requests.get(current_app.config['COGNITO_JWKS_KEYS_URL'])
    return response.json()


def check_id_token(id_token: str):
    jwks_keys = get_keys()
    token_headers = jwt.get_unverified_header(id_token)
    kid = token_headers['kid']

    used_jwk_key = None
    for key in jwks_keys['keys']:
        if kid == key['kid']:
            used_jwk_key = key

    if used_jwk_key is None:
        return TokenCheckState.INVALID

    public_key = jwk.construct(used_jwk_key)
    message, encoded_signature = str(id_token).rsplit('.', 1)

    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        return TokenCheckState.INVALID

    claims = jwt.get_unverified_claims(id_token)
    if datetime.now() > datetime.fromtimestamp(claims['exp']):
        return TokenCheckState.EXPIRED

    if 'aud' in claims and claims['aud'] != current_app.config['COGNITO_APP_CLIENT_ID']:
        return TokenCheckState.INVALID_AUD

    return TokenCheckState.VALID


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'id_token' in session:
            state = check_id_token(session['id_token'])
            if state == TokenCheckState.VALID:
                return func(*args, **kwargs)
            return redirect(url_for('admin.login', state=state))
        else:
            return redirect(url_for('admin.login'))
    return wrapper
