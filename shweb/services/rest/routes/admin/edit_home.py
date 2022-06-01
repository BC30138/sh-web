import requests

from flask import json, render_template, make_response, current_app, request
from flask_restful import Resource, reqparse, output_json

from shweb.services.rest.rest_helpers.common import auth_required

index_parser = reqparse.RequestParser()
index_parser.add_argument("device", choices=('web', 'mobile'), type=str, location="args", required=True)
index_parser.add_argument("index_code", type=dict, location="json", required=True)

index_content_parser = reqparse.RequestParser()
index_content_parser.add_argument("index_code", type=str, location="form", required=True)
index_content_parser.add_argument("delete", type=str, location="form", required=True)


class EditHomeResource(Resource):

    @auth_required
    def get(self):
        template = "admin/edit_home.html"
        base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
        index_json = requests.get(f"{base}/index/index.json").json()

        index_schema = IndexCode()
        index_code_deserial = index_schema.load(index_json)

        if 'files_list' in index_code_deserial:
            index_code_deserial['files'] = [
                [f"{item}", f"{current_app.config['AWS_CLOUD_FRONT_DOMAIN']}/index/files/{item}"]
                for item in index_code_deserial['files_list']
            ]

        return make_response(render_template(template, index_code=index_code_deserial))

    @auth_required
    def put(self):
        args = index_content_parser.parse_args()
        schema = IndexCode()
        index_code = schema.loads(args['index_code'])
        to_delete = json.loads(args['delete'])
        request.files

        index_path = "index"
        index_files_path = f"{index_path}/files"

        for filename, file in request.files.items():
            upload_file(
                file,
                f"{index_files_path}/{filename}"
            )

        upload_json(index_code, f"{index_path}/index.json")

        for item_to_delete in to_delete:
            s3_delete(
                f"{index_files_path}/{item_to_delete}"
            )

        create_invalidation(
            [f"/{index_path}/*"]
        )
        return output_json({'status': "ok"}, 200)


class PreviewResource(Resource):
    @auth_required
    def post(self):
        try:
            args = index_parser.parse_args()
            if args['device'] == "mobile":
                template = "mobile/index.html"
            else:
                template = "index.html"

            index_schema = DeviceCode()
            index_deserial = index_schema.load(args['index_code'])
            index_code = index_schema.dump(index_deserial)

            style_code = index_code['style']
            content_code = index_code['content']
            return make_response(
                render_template(template, title='Home',
                                style_code=style_code, content_code=content_code
                                ))
        except Exception:
            return output_json({"status": "error"}, 400)
