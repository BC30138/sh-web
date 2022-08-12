from flask_smorest import Api

from shweb.extensions.backend.views.public.index import blueprint as index_blueprint

def register_blueprints(api: Api):
    api.register_blueprint(index_blueprint)
