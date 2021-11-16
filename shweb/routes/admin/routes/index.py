from flask import session, redirect, url_for, request, render_template
from shweb.routes.admin.auth import auth_required

from flask_mobility.decorators import mobile_template
from shweb.routes.admin import blueprint


@blueprint.route('/')
@mobile_template('admin/{mobile/}index.html')
@auth_required
def index(template):
    return render_template(template)


@blueprint.route('/', methods=['POST'])
@auth_required
def index_form():
    if "logout" in request.form:
        session.pop('id_token')
        return redirect(url_for('admin.login'))
    return redirect(url_for('admin.index'))
