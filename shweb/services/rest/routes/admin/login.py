"""Страница логина в панель администратора"""
from typing import Optional

from flask import session, redirect, url_for, current_app, render_template, make_response, request
from flask_babel import _
from werkzeug.exceptions import InternalServerError
from warrant import Cognito
from flask_restful import Resource
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from shweb.services.rest.rest_helpers.common import auth_required, request_parser
from shweb.services.rest.rest_helpers.getters import get_identity_ctl
from shweb.services.auth_service import auth_client
from shweb.util.enums import AuthStatus


class UserScheme(Schema):
    username = fields.Str(required=False, missing=None)
    password = fields.Str(required=False, missing=None)


class ErrorStatusScheme(Schema):
    status = EnumField(AuthStatus, by_value=True, required=False, missing=None)


class ActionScheme(Schema):
    action = fields.Str(required=False, missing=None)


class LoginResource(Resource):
    @request_parser.use_kwargs(ErrorStatusScheme, location='query')
    def get(self, status: Optional[AuthStatus]):
        template = 'admin/login/login.html'

        message: Optional[str] = None
        if status is AuthStatus.EMPTY:
            message = _("The username or password field is empty")
        elif status is AuthStatus.INVALID:
            message = _("Invalid username or password")
        elif status is AuthStatus.EXPIRED:
            message = _("Your session token is expired, login again")

        return make_response(render_template(template, status=message))

    @request_parser.use_kwargs(UserScheme, location='form')
    def post(self, username: Optional[str], password: Optional[str], **_kwargs):
        identity_ctl = get_identity_ctl()
        identity_entity = identity_ctl.authenticate(username, password)
        if identity_entity is None:
            return redirect(url_for('admin.login', status=AuthStatus.EMPTY.value))
        if identity_entity.auth_status == AuthStatus.VALID:
            session['id_token'] = identity_entity.token
            return redirect(url_for('admin.index'))
        elif identity_entity.auth_status == AuthStatus.INVALID:
            return redirect(url_for('admin.login', status=AuthStatus.INVALID.value))
        elif identity_entity.auth_status == AuthStatus.CHANGE_PASSWORD:
            return redirect(url_for('admin.change-password', action="new"))
        raise InternalServerError('Such auth status is not implemented')


class LogoutResource(Resource):
    @auth_required
    def post(self):
        session.clear()
        return redirect(url_for('admin.login'))


class ForgetResource(Resource):
    @request_parser.use_kwargs(ErrorStatusScheme, location='query')
    def get(self, status: Optional[AuthStatus]):
        template = 'admin/login/forget.html'

        message: Optional[str] = None
        if status is AuthStatus.EMPTY:
            message = _("The username field is empty")
        elif status is AuthStatus.INVALID:
            message = _("Invalid username")
        elif status is AuthStatus.LIMIT:
            message = _("Attempt limit exceeded, please try after some time")
        return make_response(render_template(template, status=message))

    @request_parser.use_kwargs(UserScheme, location='form')
    def post(self, username: Optional[str], **_kwargs):
        identity_ctl = get_identity_ctl()
        identity_entity = identity_ctl.forget_password(username)

        if identity_entity is None:
            return redirect(url_for('admin.forget', status=AuthStatus.EMPTY.value))
        elif identity_entity.auth_status == AuthStatus.CHANGE_PASSWORD:
            return redirect(url_for('admin.forget-confirm', username=username))
        elif identity_entity.auth_status == AuthStatus.LIMIT:
            return redirect(url_for('admin.forget', status=AuthStatus.LIMIT.value))
        elif identity_entity.auth_status == AuthStatus.INVALID:
            return redirect(url_for('admin.forget', status=AuthStatus.INVALID.value))
        raise InternalServerError('Such auth status is not implemented')


class ForgetConfirmResource(Resource):
    @request_parser.use_kwargs(ErrorStatusScheme, location='query')
    def get(self, status: AuthStatus):
        template = 'admin/login/forget_confirm.html'

        if not request.args.get('username'):
            return redirect(url_for('admin.forget'))

        message: Optional[str] = None
        if status is AuthStatus.INVALID:
            message = _("Confirmation code invalid")
        elif status is AuthStatus.EMPTY:
            message = _("Code, password or username field is empty")
        return make_response(render_template(template, status=message))

    @request_parser.use_kwargs({
        'username': UserScheme().fields['username'],
    }, location='query')
    @request_parser.use_kwargs({
        'password': UserScheme().fields['password'],
        'code': fields.Str(required=False, missing=None),
    }, location='form')
    def post(
        self,
        username: Optional[str],
        password: Optional[str],
        code: Optional[str]
    ):
        if code and password and username:
            user = Cognito(
                user_pool_id=current_app.config['COGNITO_USERPOOL_ID'],
                client_id=current_app.config['COGNITO_APP_CLIENT_ID'],
                user_pool_region=current_app.config['COGNITO_REGION'],
                client_secret=current_app.config['COGNITO_APP_CLIENT_SECRET'],
                username=username
            )
            try:
                user.confirm_forgot_password(code, password)
                return redirect(url_for('admin.login'))
            except user.client.exceptions.CodeMismatchException:
                return redirect(
                    url_for(
                        'admin.forget-confirm',
                        username=username,
                        status=AuthStatus.INVALID.value
                    )
                )

        return redirect(url_for('admin.forget', status=AuthStatus.EMPTY.value))


class ChangePasswordResource(Resource):
    @request_parser.use_kwargs(ErrorStatusScheme, location='query')
    def get(self, status: AuthStatus):
        template = 'admin/login/change_password.html'

        message: Optional[str] = None
        if status is AuthStatus.EMPTY:
            message = _("The username or password field is empty")
        elif status is AuthStatus.INVALID:
            message = _("Invalid username or password")
        elif status is AuthStatus.EXPIRED:
            message = _("Your session token is expired, login again")

        return make_response(render_template(template, status=message))

    @request_parser.use_kwargs(ActionScheme, location='query')
    @request_parser.use_kwargs(UserScheme, location='form')
    @request_parser.use_kwargs(
        {'cur_password': fields.Str(required=False, missing=None)},
        location='form',
    )
    def post(
        self,
        action: Optional[str],
        username: Optional[str],
        password: Optional[str],
        cur_password: Optional[str],
        **_kwargs,
    ):
        if username and password and cur_password:
            user = Cognito(
                user_pool_id=current_app.config['COGNITO_USERPOOL_ID'],
                client_id=current_app.config['COGNITO_APP_CLIENT_ID'],
                user_pool_region=current_app.config['COGNITO_REGION'],
                client_secret=current_app.config['COGNITO_APP_CLIENT_SECRET'],
                username=username
            )
            try:
                if action == "new":
                    auth_client.change_password_challenge(
                        username,
                        cur_password,
                        password,
                    )
                else:
                    user.authenticate(cur_password)
                    user.change_password(cur_password, password)
                return redirect(url_for('admin.login'))
            except:
                return redirect(
                    url_for(
                        'admin.change-password',
                        status=AuthStatus.INVALID.value,
                        action=action
                    )
                )

        return redirect(url_for(
            'admin.change-password',
            status=AuthStatus.EMPTY.value,
            action=action
        ))
