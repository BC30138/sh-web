from flask import session, redirect, url_for, request, current_app, render_template
from flask_mobility.decorators import mobile_template
from warrant import Cognito
from shweb.routes.admin import blueprint


@blueprint.route('/login', methods=['GET'])
@mobile_template('admin/{mobile/}login.html')
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
