"""Рендер индекс-страницы"""
from flask import Blueprint, render_template

from shweb.services.rest.rest_helpers import mobile_template, get_index_ctl
from shweb.services.rest.schemas.index import IndexScheme

blueprint = Blueprint("index-page", __name__)


@blueprint.route('/')
@blueprint.route('/index')
@blueprint.route('/index/')
@mobile_template(['public'], 'index.html')
def index(template):
    index_clt = get_index_ctl()
    index_entity = index_clt.get()

    client_index = IndexScheme.from_entity(index_entity)['client_index']
    return render_template(
        template,
        style_code=client_index['style'],
        content_code=client_index['content'],
    )
