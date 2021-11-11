import requests
from jose import jwt, jwk
from jose.utils import base64url_decode
from datetime import datetime

from enum import Enum

from functools import wraps
from flask import Blueprint, session, redirect, url_for, request, render_template, jsonify, current_app
from flask_mobility.decorators import mobile_template

from warrant import Cognito
import botocore.exceptions

import boto3

from warrant import Cognito
import botocore.exceptions

import boto3

blueprint = Blueprint("admin", __name__)


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


@blueprint.route('/login', methods=['GET'])
@mobile_template('{mobile/}admin_login.html')
def login(template):
    return render_template(template)


@blueprint.route('/login', methods=['POST'])
def login_form():
    username = request.form['username']
    password = request.form['password']

    if username and password:
        user = Cognito(
            user_pool_id=current_app.config['COGNITO_USERPOOL_ID'],
            client_id=current_app.config['COGNITO_APP_CLIENT_ID'],
            user_pool_region=current_app.config['COGNITO_REGION'],
            client_secret=current_app.config['COGNITO_APP_CLIENT_SECRET'],
            username=username
        )
        try:
            user.authenticate(password)
            session['id_token'] = user.id_token
            return redirect(url_for('admin.index'))
        except user.client.exceptions.NotAuthorizedException:
            pass
    return redirect(url_for('admin.login'))


@blueprint.route('/')
@mobile_template('{mobile/}admin.html')
@auth_required
def index(template):
    return render_template(template)


@blueprint.route('/', methods=['POST'])
@auth_required
def index_form():
    if "logout" in request.form:
        session.pop('id_token')
        print(session.get('id_token'))
        return redirect(url_for('admin.login'))
    return redirect(url_for('admin.index'))
