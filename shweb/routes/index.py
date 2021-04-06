from flask import Blueprint, render_template

blueprint = Blueprint("index-page", __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template("index.html", title='Home')
