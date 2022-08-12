"""Рендер индекс-страницы"""
from flask import Blueprint
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow_dataclass import dataclass

blueprint = Blueprint(
    'Index',
    __name__,
    url_prefix='/index_data',
    description="Index page data"
)


@dataclass
class IndexQueryArgs:  
    is_mobile: bool


@blueprint.route('/')
class IndexResource(MethodView):
    @blueprint.arguments(IndexQueryArgs.Schema, location='query')
    def get(self, index_query_args):
        print(index_query_args.is_mobile)
        return '', 204


# @blueprint.route('/')
# @blueprint.route('/index')
# @blueprint.route('/index/')
# @mobile_template(['public'], 'index.html', include_is_mobile=True)
# def index(template, is_mobile: bool):
#     index_clt = get_index_ctl()
#     index_entity = index_clt.get()

#     client_index = IndexScheme.from_entity(index_entity, is_mobile)['client_index']
#     return render_template(
#         template,
#         style_code=client_index['style'],
#         content_code=client_index['content'],
#     )