from flask import session, redirect, request, url_for, render_template, make_response
from shweb.routes.admin.auth import auth_required
from flask_mobility.decorators import mobile_template
import werkzeug.datastructures

from flask_restful import Resource, reqparse, abort

action_parser = reqparse.RequestParser()
action_parser.add_argument("action", type=str, default="new", location="args", required=True)
action_parser.add_argument("id", type=str, location="args", required=False)

release_parser = reqparse.RequestParser()
release_parser.add_argument("cover", type=werkzeug.datastructures.FileStorage, location="files", required=True)


class ReleaseResource(Resource):
    @mobile_template('admin/{mobile/}release.html')
    @auth_required
    def get(self, template):
        release_args = action_parser.parse_args()

        return make_response(render_template(template, action=release_args['action']))

    @auth_required
    def post(self):
        # action_args = action_parser.parse_args()
        print(request.form)
        print(request.files)
        return request.form
        # if action_args['action'] == "new":
        #     release_args = release_parser.parse_args()
        #     return {"message": "success"}, 200
        # else:
        #     return abort(404)
