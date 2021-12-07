import json

from flask import session, redirect, request, url_for, render_template, make_response
from flask_mobility.decorators import mobile_template
import werkzeug.datastructures
from werkzeug.exceptions import BadRequest
from flask_restful import Resource, reqparse, abort

from shweb.routes.admin.auth import auth_required
from shweb.schemas.release import ReleaseSchema

action_parser = reqparse.RequestParser()
action_parser.add_argument("action", type=str, default="new", location="args", required=True)
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
        release_args = release_parser.parse_args()

        release_object = ReleaseSchema()
        release_deserial = release_object.load(
            json.loads(release_args['release'])
        )
        return redirect(url_for("admin.index"))
