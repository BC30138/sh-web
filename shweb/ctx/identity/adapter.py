"""Адаптер для доступа к системе аутентификации"""

import abc

import warrant
from botocore.exceptions import ClientError

from shweb.ctx.identity.model import IdentityEntity
from shweb.services.auth_service import auth_client
from shweb.util.enums import AuthStatus


class IIdentityAdapter(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def authenticate(cls, username: str, password: str) -> IdentityEntity:
        raise NotImplementedError


class IdentityAdapter(IIdentityAdapter):
    @classmethod
    def authenticate(cls, username: str, password: str) -> IdentityEntity:
        user = auth_client.get_user(username)
        identity_kwargs = {
            'username': username,
            'password': password,
        }

        try:
            user.authenticate(password)
            identity_kwargs['token'] = user.id_token
            identity_kwargs['auth_status'] = AuthStatus.VALID
        except user.client.exceptions.NotAuthorizedException:
            identity_kwargs['auth_status'] = AuthStatus.INVALID
        except (warrant.exceptions.ForceChangePasswordException, ClientError):
            identity_kwargs['auth_status'] = AuthStatus.FORCE_CHANGE_PASSWORD

        return IdentityEntity(**identity_kwargs)
