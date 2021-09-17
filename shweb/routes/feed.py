from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template
from flask_babel import get_locale
blueprint = Blueprint("feed", __name__)


@blueprint.route('/')
@mobile_template('{mobile/}feed.html')
def index(template):
    return render_template(template, title='Feed')
