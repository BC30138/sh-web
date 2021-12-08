import json

from flask import redirect, url_for, render_template, make_response
from flask_mobility.decorators import mobile_template
import werkzeug.datastructures
from werkzeug.exceptions import BadRequest
from flask_restful import Resource, reqparse, abort

from shweb.routes.admin.auth import auth_required
from shweb.schemas.release import ReleaseSchema
from shweb.schemas.release_list import ReleaseListSchema, ReleaseListItemSchema
from shweb.utils import get_raw_release_list, create_invalidation, upload_json, upload_file, delete_prefix

action_parser = reqparse.RequestParser()
action_parser.add_argument("action", type=str, choices=('new', 'edit', 'delete'), location="args", required=True)
action_parser.add_argument("id", type=str, location="args", required=False)

release_parser = reqparse.RequestParser()
release_parser.add_argument("release", type=str, location="form", required=True)
release_parser.add_argument("cover", type=werkzeug.datastructures.FileStorage, location="files", required=True)
release_parser.add_argument("og", type=werkzeug.datastructures.FileStorage, location="files", required=True)


class ReleaseResource(Resource):
    @mobile_template('admin/{mobile/}release.html')
    @auth_required
    def get(self, template):
        try:
            release_args = action_parser.parse_args()
        except BadRequest as e:
            return redirect(url_for('admin.release', action="new"))
        return make_response(render_template(template, action=release_args['action']))

    @auth_required
    def post(self):
        action_args = action_parser.parse_args()

        release_list_path = "releases/release-list.json"
        if action_args['action'] == "delete":
            response = get_raw_release_list()
            list_schema = ReleaseListSchema()
            list_schema_deserial = list_schema.load(response)

            list_schema_deserial['releases'] = list(
                filter(lambda i: i['id'] != action_args['id'], list_schema_deserial['releases'])
            )

            delete_prefix(f"releases/{action_args['id']}/")
            upload_json(list_schema_deserial, release_list_path)
            create_invalidation([f"/{release_list_path}"])

            return redirect(url_for("admin.index"))

        release_args = release_parser.parse_args()
        release_schema = ReleaseSchema()
        release_schema_deserial = release_schema.load(
            json.loads(release_args['release'])
        )
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

        if action_args['action'] == "new":
            response = get_raw_release_list()
            list_schema = ReleaseListSchema()
            list_schema_deserial = list_schema.load(response)

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

        elif action_args['action'] == "edit":
            if action_args['id'] != release_schema_deserial['release_id']:
                response = get_raw_release_list()
                list_schema = ReleaseListSchema()
                list_schema_deserial = list_schema.load(response)

                list_schema_deserial['releases'] = list(
                    filter(lambda i: i['id'] != action_args['id'], list_schema_deserial['releases'])
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

                delete_prefix(f"releases/{action_args['id']}/")
                upload_json(list_schema_deserial, release_list_path)
                create_invalidation([f"/{release_list_path}"])
            else:
                create_invalidation([f"/{release_path}/*"])

            return abort(400)
        return redirect(url_for("admin.index"))
