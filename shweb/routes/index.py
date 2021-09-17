from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template
blueprint = Blueprint("index-page", __name__)

from flask_babel import get_locale


@blueprint.route('/')
@blueprint.route('/index')
@mobile_template('{mobile/}index.html')
def index(template):
    return render_template(template, title='Home', locale=get_locale())
