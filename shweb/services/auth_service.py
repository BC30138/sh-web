"""Сервис аутентификации"""

from enum import Enum
from datetime import datetime
from typing import Optional
import hmac
import hashlib
import base64

import boto3
import requests
from jose import jwt, jwk
from jose.utils import base64url_decode

from shweb.config import Config


class AuthStatus(Enum):
    valid = 'valid'
    invalid = 'invalid'
    expired = 'expired'
    invalid_aud = 'invalid_aud'
    empty = 'empty'
    limit = 'limit'


class AuthService:
    def __init__(
        self,
        jwks_keys_url: str,
        app_client_id: str,
        userpool_id: str,
        client_secret: str,
        access_key: str,
        secret_key: str,
        region: str,
    ):
        self._jwks_keys_url = jwks_keys_url
        self._app_client_id = app_client_id
        self._userpool_id = userpool_id
        self._client_secret = client_secret
        self._access_key = access_key
        self._secret_key = secret_key
        self._region = region

    def get_keys(self) -> Optional[dict]:
        response = requests.get(self._jwks_keys_url)
        return response.json()

    def check_id_token(self, id_token: str) -> AuthStatus:
        jwks_keys = self.get_keys()
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

        if 'aud' in claims and claims['aud'] != self._app_client_id:
            return AuthStatus.invalid_aud

        return AuthStatus.valid

    def change_password_challenge(
            self,
            username,
            temp_password,
            new_password,
    ):

        secret_hash = self._get_secret_hash(username)
        cognito = boto3.client(
            'cognito-idp',
            region_name=self._region,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
        )
        auth_response = cognito.admin_initiate_auth(
            UserPoolId=self._userpool_id,
            ClientId=self._app_client_id,
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
            UserPoolId=self._userpool_id,
            ClientId=self._app_client_id,
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

    def _get_secret_hash(self, username):
        msg = username + self._app_client_id
        dig = hmac.new(str(self._client_secret).encode('utf-8'),
                       msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2


auth_client = AuthService(
    jwks_keys_url=Config.COGNITO_JWKS_KEYS_URL,
    app_client_id=Config.COGNITO_APP_CLIENT_ID,
    userpool_id=Config.COGNITO_USERPOOL_ID,
    client_secret=Config.COGNITO_APP_CLIENT_SECRET,
    access_key=Config.AWS_ACCESS_KEY,
    secret_key=Config.AWS_SECRET_KEY,
    region=Config.AWS_REGION,
)
