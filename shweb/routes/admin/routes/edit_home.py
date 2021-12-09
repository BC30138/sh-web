from flask import render_template, make_response
from flask_mobility.decorators import mobile_template
from flask_restful import Resource

from shweb.routes.admin.auth import auth_required


class EditHomeResource(Resource):
    @mobile_template('admin/{mobile/}edit_home.html')
    @auth_required
    def get(self, template):
        print('a')
        return make_response(render_template(template))
