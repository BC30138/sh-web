from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template
blueprint = Blueprint("index-page", __name__)


@blueprint.route('/')
@blueprint.route('/index')
@mobile_template('{mobile/}index.html')
def index(template):
    return render_template(template, title='Home')


# def index():
#     return render_template("mobile/index.html")
