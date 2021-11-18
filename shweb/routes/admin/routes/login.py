
from enum import Enum
from flask import session, redirect, url_for, current_app, render_template, make_response
from flask_mobility.decorators import mobile_template
from flask_babel import _
from warrant import Cognito


from flask_restful import Resource, reqparse

login_parser = reqparse.RequestParser()
login_parser.add_argument("username", type=str, location="form", required=True)
login_parser.add_argument("password", type=str, location="form", required=True)

error_status_parser = reqparse.RequestParser()
error_status_parser.add_argument("status", type=str, location="args", required=False)


class AuthErrorStatus(Enum):
    invalid = 1
    empty = 2


class LoginResource(Resource):
    @mobile_template('admin/{mobile/}login.html')
    def get(self, template):
        status_args = error_status_parser.parse_args()
        status: AuthErrorStatus = None
        if status_args['status']:
            try:
                status = AuthErrorStatus[status_args['status']]
            except KeyError:
                pass

        message: str = None
        if status is AuthErrorStatus.empty:
            message = _("The username or password field is empty")
        elif status is AuthErrorStatus.invalid:
            message = _("Invalid username or password")

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
                return redirect(url_for('admin.login', status=AuthErrorStatus.invalid.name))

        return redirect(url_for('admin.login', status=AuthErrorStatus.empty.name))
