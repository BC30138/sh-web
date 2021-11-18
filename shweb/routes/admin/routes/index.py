from flask import session, redirect, url_for, render_template, make_response
from shweb.routes.admin.auth import auth_required

from flask_mobility.decorators import mobile_template

from flask_restful import Resource, reqparse

index_parser = reqparse.RequestParser()
index_parser.add_argument("event", type=str, location="form", required=True)


class IndexResource(Resource):
    @mobile_template('admin/{mobile/}index.html')
    @auth_required
    def get(self, template):
        return make_response(render_template(template))

    @auth_required
    def post(self):
        event_args = index_parser.parse_args()
        if event_args.get("event") == "logout":
            session.pop('id_token')
            return redirect(url_for('admin.login'))
        return redirect(url_for('admin.index'))
