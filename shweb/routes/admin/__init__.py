from flask import Blueprint, render_template, current_app, jsonify
from flask_mobility.decorators import mobile_template
from flask_cognito import cognito_auth_required, current_user, current_cognito_jwt, cognito_group_permissions

blueprint = Blueprint("admin", __name__)


# @blueprint.route('/')
# @mobile_template('{mobile/}admin_login.html')
# def index(template):
#     return render_template(template)


@blueprint.route('/', methods=['GET', 'POST'])
@cognito_auth_required
@cognito_group_permissions(['admin'])
def index(template):
    return jsonify({
        'cognito_username': current_cognito_jwt['username'],   # from cognito pool
        'user_id': current_user.id,   # from your database
    })
