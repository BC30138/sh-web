"""Страница логина в панель администратора"""
from typing import Optional

from botocore.exceptions import ClientError
from flask import session, redirect, url_for, current_app, render_template, make_response, request
from flask_babel import _
from warrant import Cognito
import warrant
from flask_restful import Resource
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from shweb.services.rest.rest_helpers.common import auth_required, request_parser
from shweb.services.auth_service import AuthStatus, auth_client


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
        if status is AuthStatus.empty:
            message = _("The username or password field is empty")
        elif status is AuthStatus.invalid:
            message = _("Invalid username or password")
        elif status is AuthStatus.expired:
            message = _("Your session token is expired, login again")

        return make_response(render_template(template, status=message))

    @request_parser.use_kwargs(UserScheme, location='form')
    def post(self, username: Optional[str], password: Optional[str], **_kwargs):
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
                return redirect(url_for('admin.login', status=AuthStatus.invalid.name))
            except (warrant.exceptions.ForceChangePasswordException, ClientError):
                return redirect(url_for('admin.change-password', action="new"))

        return redirect(url_for('admin.login', status=AuthStatus.empty.value))


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
        if status is AuthStatus.empty:
            message = _("The username field is empty")
        elif status is AuthStatus.invalid:
            message = _("Invalid username")
        elif status is AuthStatus.limit:
            message = _("Attempt limit exceeded, please try after some time")
        return make_response(render_template(template, status=message))

    @request_parser.use_kwargs(UserScheme, location='form')
    def post(self, username: Optional[str], **_kwargs):
        if username:
            user = Cognito(
                user_pool_id=current_app.config['COGNITO_USERPOOL_ID'],
                client_id=current_app.config['COGNITO_APP_CLIENT_ID'],
                user_pool_region=current_app.config['COGNITO_REGION'],
                client_secret=current_app.config['COGNITO_APP_CLIENT_SECRET'],
                username=username
            )
            try:
                user.initiate_forgot_password()
                return redirect(url_for('admin.forget-confirm', username=username))
            except user.client.exceptions.LimitExceededException:
                return redirect(url_for('admin.forget', status=AuthStatus.limit.name))

        return redirect(url_for('admin.forget', status=AuthStatus.empty.name))


class ForgetConfirmResource(Resource):
    @request_parser.use_kwargs(ErrorStatusScheme, location='query')
    def get(self, status: AuthStatus):
        template = 'admin/login/forget_confirm.html'

        if not request.args.get('username'):
            return redirect(url_for('admin.forget'))

        message: Optional[str] = None
        if status is AuthStatus.invalid:
            message = _("Confirmation code invalid")
        elif status is AuthStatus.empty:
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
                        status=AuthStatus.invalid.name
                    )
                )

        return redirect(url_for('admin.forget', status=AuthStatus.empty.name))


class ChangePasswordResource(Resource):
    @request_parser.use_kwargs(ErrorStatusScheme, location='query')
    def get(self, status: AuthStatus):
        template = 'admin/login/change_password.html'

        message: Optional[str] = None
        if status is AuthStatus.empty:
            message = _("The username or password field is empty")
        elif status is AuthStatus.invalid:
            message = _("Invalid username or password")
        elif status is AuthStatus.expired:
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
                        status=AuthStatus.invalid.name,
                        action=action
                    )
                )

        return redirect(url_for(
            'admin.change-password',
            status=AuthStatus.empty.name,
            action=action
        ))
