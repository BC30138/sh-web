import json
import requests

from flask import redirect, url_for, render_template, make_response, current_app
from flask_mobility.decorators import mobile_template
import werkzeug.datastructures
from werkzeug.exceptions import BadRequest
from flask_restful import Resource, reqparse, output_json

from shweb.routes.admin.auth import auth_required
from shweb.schemas.release import ReleaseSchema, EditReleaseSchema
from shweb.schemas.release_list import ReleaseListSchema, ReleaseListItemSchema
from shweb.utils import get_raw_release_list, create_invalidation, upload_json, upload_file, delete_prefix

action_parser = reqparse.RequestParser()
action_parser.add_argument("action", type=str, choices=('new', 'edit'), location="args", required=True)
action_parser.add_argument("id", type=str, location="args", required=False)

id_parser = action_parser.copy()
id_parser.remove_argument('action')

release_parser = reqparse.RequestParser()
release_parser.add_argument("release", type=str, location="form", required=True)
release_parser.add_argument("cover", type=werkzeug.datastructures.FileStorage, location="files", required=True)
release_parser.add_argument("og", type=werkzeug.datastructures.FileStorage, location="files", required=True)

update_release_parser = release_parser.copy()
update_release_parser.replace_argument(
    "cover", type=werkzeug.datastructures.FileStorage, location="files", required=False)
update_release_parser.replace_argument(
    "og", type=werkzeug.datastructures.FileStorage, location="files", required=False)


class ReleaseResource(Resource):
    @mobile_template('admin/{mobile/}release.html')
    @auth_required
    def get(self, template):
        try:
            release_args = action_parser.parse_args()
        except BadRequest as e:
            return redirect(url_for('admin.release', action="new"))

        release = {}
        if release_args['action'] == "edit":
            if 'id' not in release_args:
                return redirect(url_for('admin.release', action="new"))
            release = release_args['id']
            base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
            release_json: dict = requests.get(f"{base}/releases/{release}/info.json").json()
            schema = EditReleaseSchema()
            schema_deserial = schema.load(release_json)
            release = schema.dump(schema_deserial)

        return make_response(
            render_template(
                template,
                action=release_args['action'],
                release=release
            )
        )

    @auth_required
    def post(self):
        release_args = release_parser.parse_args()

        release_schema = ReleaseSchema()
        release_schema_deserial = release_schema.load(
            json.loads(release_args['release'])
        )

        response = get_raw_release_list()
        list_schema = ReleaseListSchema()
        list_schema_deserial = list_schema.load(response)

        if release_schema_deserial['release_id'] in [x['id'] for x in list_schema_deserial['releases']]:
            return output_json({'status': "Release with this name alredy exists"}, 400)

        release_list_path = "releases/release-list.json"
        release_path = f"releases/{release_schema_deserial['release_id']}"

        upload_json(
            release_schema_deserial,
            f"{release_path}/info.json"
        )
        upload_file(
            release_args['cover'],
            f"{release_path}/cover.jpg"
        )
        upload_file(
            release_args['og'],
            f"{release_path}/og.jpg"
        )

        item_schema = ReleaseListItemSchema()
        item_schema_deserial = item_schema.load(
            {
                "id": release_schema_deserial['release_id'],
                "name": release_schema_deserial['release_name'],
                "type": release_schema_deserial['type']
            }
        )
        list_schema_deserial['releases'].append(item_schema_deserial)

        upload_json(list_schema_deserial, release_list_path)
        create_invalidation([f"/{release_list_path}"])

        return output_json({'status': "ok"}, 200)

    @auth_required
    def put(self):
        args = id_parser.parse_args()
        release_args = update_release_parser.parse_args()

        release_schema = ReleaseSchema()
        release_schema_deserial = release_schema.load(
            json.loads(release_args['release'])
        )

        release_list_path = "releases/release-list.json"
        release_path = f"releases/{release_schema_deserial['release_id']}"

        upload_json(
            release_schema_deserial,
            f"{release_path}/info.json"
        )
        if release_args['cover'] is not None:
            upload_file(
                release_args['cover'],
                f"{release_path}/cover.jpg"
            )
        if release_args['og'] is not None:
            upload_file(
                release_args['og'],
                f"{release_path}/og.jpg"
            )

        if args['id'] != release_schema_deserial['release_id']:
            response = get_raw_release_list()
            list_schema = ReleaseListSchema()
            list_schema_deserial = list_schema.load(response)

            if release_schema_deserial['release_id'] in [x['id'] for x in list_schema_deserial['releases']]:
                return output_json({'status': "Release with this name alredy exists"}, 400)

            list_schema_deserial['releases'] = list(
                filter(lambda i: i['id'] != args['id'], list_schema_deserial['releases'])
            )

            item_schema = ReleaseListItemSchema()
            item_schema_deserial = item_schema.load(
                {
                    "id": release_schema_deserial['release_id'],
                    "name": release_schema_deserial['release_name'],
                    "type": release_schema_deserial['type']
                }
            )
            list_schema_deserial['releases'].append(item_schema_deserial)

            delete_prefix(f"releases/{args['id']}/")
            upload_json(list_schema_deserial, release_list_path)
            create_invalidation([f"/{release_list_path}"])
        create_invalidation([f"/{release_path}/*"])

        return output_json({'status': "ok"}, 200)

    @auth_required
    def delete(self):
        args = id_parser.parse_args()
        release_list_path = "releases/release-list.json"

        response = get_raw_release_list()
        list_schema = ReleaseListSchema()
        list_schema_deserial = list_schema.load(response)

        list_schema_deserial['releases'] = list(
            filter(lambda i: i['id'] != args['id'], list_schema_deserial['releases'])
        )

        delete_prefix(f"releases/{args['id']}/")
        upload_json(list_schema_deserial, release_list_path)
        create_invalidation([f"/{release_list_path}"])

        return output_json({'status': "ok"}, 200)
