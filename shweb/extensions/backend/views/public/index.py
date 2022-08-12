"""Рендер индекс-страницы"""
from flask import Blueprint
from flask.views import MethodView
from flask_smorest import Blueprint

from shweb.extensions.backend.models.index import IndexQueryArgs


blueprint = Blueprint(
    'Index',
    __name__,
    url_prefix='/index_data',
    description="Index page data"
)


@blueprint.route('/')
class IndexResource(MethodView):
    @blueprint.arguments(IndexQueryArgs.Schema, location='query')
    def get(self, index_query_args):
        print(index_query_args)
        return '', 204
