from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template
blueprint = Blueprint("feed", __name__)


@blueprint.route('/feed')
@mobile_template('{mobile/}feed.html')
def index(template):
    return render_template(template, title='Feed')
