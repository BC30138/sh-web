"""Сервис аутентификации"""

from enum import Enum
from datetime import datetime
from typing import Optional

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
    ):
        self._jwks_keys_url = jwks_keys_url
        self._app_client_id = app_client_id

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


auth_client = AuthService(
    jwks_keys_url=Config.COGNITO_JWKS_KEYS_URL,
    app_client_id=Config.COGNITO_APP_CLIENT_ID,
)
