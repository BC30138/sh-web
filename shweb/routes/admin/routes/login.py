
from flask import session, redirect, url_for, current_app, render_template, make_response, request
from flask_babel import _
from warrant import Cognito
import warrant
from flask_restful import Resource, reqparse
from flask_mobility.decorators import mobile_template

from shweb.routes.admin.auth import AuthStatus, auth_required, change_password_challenge

login_parser = reqparse.RequestParser()
login_parser.add_argument("username", type=str, location="form", required=True)
login_parser.add_argument("password", type=str, location="form", required=True)

error_status_parser = reqparse.RequestParser()
error_status_parser.add_argument("status", type=str, location="args", required=False)


class LoginResource(Resource):
    @mobile_template('admin/{mobile/}/login/login.html')
    def get(self, template):
        status_args = error_status_parser.parse_args()
        status: AuthStatus = None
        if status_args.get('status'):
            try:
                status = AuthStatus[status_args['status']]
            except KeyError:
                pass

        message: str = None
        if status is AuthStatus.empty:
            message = _("The username or password field is empty")
        elif status is AuthStatus.invalid:
            message = _("Invalid username or password")
        elif status is AuthStatus.expired:
            message = _("Your session token is expired, login again")

        return make_response(render_template(template, status=message))

    def post(self):
        auth_args = login_parser.parse_args()

        if auth_args['username'] and auth_args['password']:
            user = Cognito(
                user_pool_id=current_app.config['COGNITO_USERPOOL_ID'],
                client_id=current_app.config['COGNITO_APP_CLIENT_ID'],
                user_pool_region=current_app.config['COGNITO_REGION'],
                client_secret=current_app.config['COGNITO_APP_CLIENT_SECRET'],
                username=auth_args['username']
            )
            try:
                user.authenticate(auth_args['password'])
                session['id_token'] = user.id_token
                return redirect(url_for('admin.index'))
            except user.client.exceptions.NotAuthorizedException:
                return redirect(url_for('admin.login', status=AuthStatus.invalid.name))
            except warrant.exceptions.ForceChangePasswordException:
                return redirect(url_for('admin.change-password', action="new"))

        return redirect(url_for('admin.login', status=AuthStatus.empty.name))


class LogoutResource(Resource):
    @auth_required
    def post(self):
        session.clear()
        return redirect(url_for('admin.login'))


username_parser = reqparse.RequestParser()
username_parser.add_argument("username", type=str, location="form", required=True)


class ForgetResource(Resource):
    @mobile_template('admin/{mobile/}/login/forget.html')
    def get(self, template):
        status_args = error_status_parser.parse_args()
        status: AuthStatus = None
        if status_args['status']:
            try:
                status = AuthStatus[status_args['status']]
            except KeyError:
                pass

        message: str = None
        if status is AuthStatus.empty:
            message = _("The username field is empty")
        elif status is AuthStatus.invalid:
            message = _("Invalid username")
        elif status is AuthStatus.limit:
            message = _("Attempt limit exceeded, please try after some time")
        return make_response(render_template(template, status=message))

    def post(self):
        auth_args = username_parser.parse_args()

        if auth_args['username']:
            user = Cognito(
                user_pool_id=current_app.config['COGNITO_USERPOOL_ID'],
                client_id=current_app.config['COGNITO_APP_CLIENT_ID'],
                user_pool_region=current_app.config['COGNITO_REGION'],
                client_secret=current_app.config['COGNITO_APP_CLIENT_SECRET'],
                username=auth_args['username']
            )
            try:
                user.initiate_forgot_password()
                return redirect(url_for('admin.forget-confirm', username=auth_args['username']))
            except user.client.exceptions.LimitExceededException:
                return redirect(url_for('admin.forget', status=AuthStatus.limit.name))

        return redirect(url_for('admin.forget', status=AuthStatus.empty.name))


confirm_parser = reqparse.RequestParser()
confirm_parser.add_argument("username", type=str, location="args", required=True)
confirm_parser.add_argument("code", type=str, location="form", required=True)
confirm_parser.add_argument("password", type=str, location="form", required=True)


class ForgetConfirmResource(Resource):
    @mobile_template('admin/{mobile/}/login/forget_confirm.html')
    def get(self, template):
        if not request.args.get('username'):
            return redirect(url_for('admin.forget'))

        status_args = error_status_parser.parse_args()
        status: AuthStatus = None
        if status_args['status']:
            try:
                status = AuthStatus[status_args['status']]
            except KeyError:
                pass

        message: str = None
        if status is AuthStatus.invalid:
            message = _("Confirmation code invalid")
        elif status is AuthStatus.empty:
            message = _("Code or password field is empty")
        return make_response(render_template(template, status=message))

    def post(self):
        auth_args = confirm_parser.parse_args()

        if auth_args['code'] and auth_args['password']:
            user = Cognito(
                user_pool_id=current_app.config['COGNITO_USERPOOL_ID'],
                client_id=current_app.config['COGNITO_APP_CLIENT_ID'],
                user_pool_region=current_app.config['COGNITO_REGION'],
                client_secret=current_app.config['COGNITO_APP_CLIENT_SECRET'],
                username=auth_args['username']
            )
            try:
                user.confirm_forgot_password(auth_args['code'], auth_args['password'])
                return redirect(url_for('admin.login'))
            except user.client.exceptions.CodeMismatchException:
                return redirect(url_for('admin.forget-confirm', username=auth_args['username'], status=AuthStatus.invalid.name))

        return redirect(url_for('admin.forget', status=AuthStatus.empty.name))


action_parser = reqparse.RequestParser()
action_parser.add_argument("action", type=str, location="args", required=False)

change_parser = reqparse.RequestParser()
change_parser.add_argument("username", type=str, location="form", required=True)
change_parser.add_argument("cur_password", type=str, location="form", required=True)
change_parser.add_argument("password", type=str, location="form", required=True)


class ChangePasswordResource(Resource):
    @mobile_template('admin/{mobile/}/login/change_password.html')
    def get(self, template):
        status_args = error_status_parser.parse_args()

        status: AuthStatus = None
        if status_args['status']:
            try:
                status = AuthStatus[status_args['status']]
            except KeyError:
                pass

        message: str = None
        if status is AuthStatus.empty:
            message = _("The username or password field is empty")
        elif status is AuthStatus.invalid:
            message = _("Invalid username or password")
        elif status is AuthStatus.expired:
            message = _("Your session token is expired, login again")

        return make_response(render_template(template, status=message))

    def post(self):
        auth_args = change_parser.parse_args()
        action_args = action_parser.parse_args()

        if auth_args['username'] and auth_args['password'] and auth_args['cur_password']:
            user = Cognito(
                user_pool_id=current_app.config['COGNITO_USERPOOL_ID'],
                client_id=current_app.config['COGNITO_APP_CLIENT_ID'],
                user_pool_region=current_app.config['COGNITO_REGION'],
                client_secret=current_app.config['COGNITO_APP_CLIENT_SECRET'],
                username=auth_args['username']
            )
            try:
                if action_args.get('action') == "new":
                    change_password_challenge(
                        current_app.config['COGNITO_USERPOOL_ID'],
                        current_app.config['COGNITO_APP_CLIENT_ID'],
                        current_app.config['COGNITO_APP_CLIENT_SECRET'],
                        current_app.config['AWS_ACCESS_KEY'],
                        current_app.config['AWS_SECRET_KEY'],
                        auth_args['username'],
                        auth_args['cur_password'],
                        auth_args['password']
                    )
                else:
                    user.authenticate(auth_args['cur_password'])
                    user.change_password(auth_args['cur_password'], auth_args['password'])
                return redirect(url_for('admin.login'))
            except Exception as e:
                return redirect(url_for('admin.change-password', status=AuthStatus.invalid.name, action=action_args.get('action')))

        return redirect(url_for('admin.change-password', status=AuthStatus.empty.name, action=action_args.get('action')))
