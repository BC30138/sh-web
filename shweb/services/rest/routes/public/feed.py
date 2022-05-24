"""Рендер страницы новостей"""
from flask import Blueprint, render_template

from shweb.services.rest.rest_helpers import mobile_template


blueprint = Blueprint("feed", __name__)


@blueprint.route('/')
@mobile_template(['public'], 'feed.html')
def index(template):
    return render_template(template, title='Feed')
