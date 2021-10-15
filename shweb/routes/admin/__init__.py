from flask import Blueprint, render_template, current_app
from flask_login import LoginManager, current_user, login_required
from flask_mobility.decorators import mobile_template

blueprint = Blueprint("admin", __name__)


USER_POOL_ID = "eu-central-1_R7kMPFbB3"
CLIENT_ID = "35g94vf37ro8d2m8ab1nilld18"


@blueprint.route('/')
@login_required
@mobile_template('{mobile/}admin_login.html')
def index(template):
    return render_template(template)
