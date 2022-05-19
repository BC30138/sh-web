import requests
from functools import wraps
from datetime import datetime
from enum import Enum
import hmac
import hashlib
import base64


from flask import session, redirect, url_for, current_app
from jose import jwt, jwk
from jose.utils import base64url_decode
import boto3


class AuthStatus(Enum):
    valid = 1
    invalid = 2
    expired = 3
    invalid_aud = 4
    empty = 5
    limit = 6


def get_user_info_from_token():
    return jwt.get_unverified_claims(session['id_token'])


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
        return AuthStatus.invalid

    public_key = jwk.construct(used_jwk_key)
    message, encoded_signature = str(id_token).rsplit('.', 1)

    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        return AuthStatus.invalid

    claims = jwt.get_unverified_claims(id_token)
    if datetime.now() > datetime.fromtimestamp(claims['exp']):
        return AuthStatus.expired

    if 'aud' in claims and claims['aud'] != current_app.config['COGNITO_APP_CLIENT_ID']:
        return AuthStatus.invalid_aud

    return AuthStatus.valid


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'id_token' in session:
            state = check_id_token(session['id_token'])
            if state == AuthStatus.valid:
                return func(*args, **kwargs)
            return redirect(url_for('admin.login', status=state.name))
        else:
            return redirect(url_for('admin.login'))
    return wrapper


def get_secret_hash(username, client_id, client_secret,):
    msg = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def change_password_challenge(
    user_pool_id,
    client_id,
    client_secret,
    aws_access_key_id,
    aws_secret_access_key,
    username,
    temp_password,
    new_password,
):
    secret_hash = get_secret_hash(username, client_id, client_secret)
    cognito = boto3.client(
        'cognito-idp',
        region_name=current_app.config['AWS_REGION'],
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    auth_response = cognito.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': username,
            'SECRET_HASH': secret_hash,
            'PASSWORD': temp_password
        }
    )

    if 'ChallengeName' not in auth_response:
        raise Exception('This user has already changed the password')

    if auth_response['ChallengeName'] != 'NEW_PASSWORD_REQUIRED':
        raise Exception("This script supports only the 'NEW_PASSWORD_REQUIRED' challenge")

    challenge_response = cognito.admin_respond_to_auth_challenge(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        ChallengeName=auth_response['ChallengeName'],
        Session=auth_response['Session'],
        ChallengeResponses={
            'USERNAME': username,
            'NEW_PASSWORD': new_password,
            'SECRET_HASH': secret_hash,
            'userAttributes.nickname': username
        }
    )

    return username, new_password, challenge_response
