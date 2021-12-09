import requests

from flask import render_template, make_response, current_app
from flask_restful import Resource, reqparse

from shweb.routes.admin.auth import auth_required
from shweb.schemas.index_code import DeviceCode, IndexCode

index_parser = reqparse.RequestParser()
index_parser.add_argument("device", choices=('web', 'mobile'), type=str, location="args", required=True)
index_parser.add_argument("style", type=str, location="json", required=True)
index_parser.add_argument("content", type=str, location="files", required=True)


class EditHomeResource(Resource):

    @auth_required
    def get(self):
        template = "admin/edit_home.html"
        base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
        index_json = requests.get(f"{base}/index/index.json").json()

        index_schema = IndexCode()
        index_code_deserial = index_schema.load(index_json)
        return make_response(render_template(template, index_code=index_code_deserial))


class PreviewResource(Resource):
    # @mobile_template('{mobile/}index.html')
    @auth_required
    def post(self):
        args = index_parser.parse_args()
        if args['device'] == "mobile":
            template = "mobile/index.html"
        else:
            template = "index.html"

        index_schema = DeviceCode()
        index_deserial = index_schema.load({
            "style": args['style'],
            "content": args['content']
        })
        index_code = index_schema.dump(index_deserial)

        style_code = index_code['style']
        content_code = index_code['content']
        return make_response(
            render_template(template, title='Home',
                            style_code=style_code, content_code=content_code
                            ))
