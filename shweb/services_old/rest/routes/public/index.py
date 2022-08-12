"""Рендер индекс-страницы"""
from flask import Blueprint, render_template

from shweb.extensions.rest.rest_helpers.mobile import mobile_template
from shweb.extensions.rest.rest_helpers.getters import get_index_ctl
from shweb.extensions.rest.schemas.index import IndexScheme

blueprint = Blueprint("index-page", __name__)


@blueprint.route('/')
@blueprint.route('/index')
@blueprint.route('/index/')
@mobile_template(['public'], 'index.html', include_is_mobile=True)
def index(template, is_mobile: bool):
    index_clt = get_index_ctl()
    index_entity = index_clt.get()

    client_index = IndexScheme.from_entity(index_entity, is_mobile)['client_index']
    return render_template(
        template,
        style_code=client_index['style'],
        content_code=client_index['content'],
    )
