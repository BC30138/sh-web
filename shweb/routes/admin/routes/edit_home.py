import requests

from flask import json, render_template, make_response, current_app, request
from flask_restful import Resource, reqparse, output_json

from shweb.routes.admin.auth import auth_required
from shweb.schemas.index_code import DeviceCode, IndexCode

index_parser = reqparse.RequestParser()
index_parser.add_argument("device", choices=('web', 'mobile'), type=str, location="args", required=True)
index_parser.add_argument("style", type=str, location="json", required=True)
index_parser.add_argument("content", type=str, location="files", required=True)

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
                [f"{item}", f"{current_app.config['AWS_CLOUD_FRONT_DOMAIN']}/index/files/{item}"] for item in index_code_deserial['files_list']]
        return make_response(render_template(template, index_code=index_code_deserial))

    @auth_required
    def put(self):
        args = index_content_parser.parse_args()
        schema = IndexCode()
        index_code = schema.loads(args['index_code'])
        to_delete = args['delete']
        request.files

        index_path = "index"
        index_files_path = f"{index_path}/files"
        # release_path = f"releases/{release_schema_deserial['release_id']}"

        # upload_json(
        #     release_schema_deserial,
        #     f"{release_path}/info.json"
        # )
        # if release_args['cover'] is not None:
        #     upload_file(
        #         release_args['cover'],
        #         f"{release_path}/cover.jpg"
        #     )
        # if release_args['og'] is not None:
        #     upload_file(
        #         release_args['og'],
        #         f"{release_path}/og.jpg"
        #     )

        # if args['id'] != release_schema_deserial['release_id']:
        #     response = get_raw_release_list()
        #     list_schema = ReleaseListSchema()
        #     list_schema_deserial = list_schema.load(response)

        #     if release_schema_deserial['release_id'] in [x['id'] for x in list_schema_deserial['releases']]:
        #         return output_json({'status': "Release with this name alredy exists"}, 400)

        #     list_schema_deserial['releases'] = list(
        #         filter(lambda i: i['id'] != args['id'], list_schema_deserial['releases'])
        #     )

        #     item_schema = ReleaseListItemSchema()
        #     item_schema_deserial = item_schema.load(
        #         {
        #             "id": release_schema_deserial['release_id'],
        #             "name": release_schema_deserial['release_name'],
        #             "type": release_schema_deserial['type']
        #         }
        #     )
        #     list_schema_deserial['releases'].append(item_schema_deserial)

        #     delete_prefix(f"releases/{args['id']}/")
        #     upload_json(list_schema_deserial, release_list_path)
        #     create_invalidation([f"/{release_list_path}"])
        # create_invalidation([f"/{release_path}/*"])

        return output_json({'status': "ok"}, 400)
        # return output_json({'status': "ok"}, 200)


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
