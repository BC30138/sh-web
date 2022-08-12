"""Взаимодействия со страницей индекса панели администратора"""

from flask import render_template, make_response
from flask_restful import Resource
from flask_apispec import use_kwargs
from marshmallow import fields

from shweb.extensions.rest.rest_helpers.common import auth_required
from shweb.extensions.rest.rest_helpers.getters import get_release_ctl
from shweb.extensions.rest.schemas.release import ReleaseListScheme


class IndexResource(Resource):
    template = 'admin/index.html'

    @auth_required
    def get(self):
        return make_response(render_template(self.template))

    @auth_required
    @use_kwargs(
        {'releases': fields.Dict(required=True)},
        location='json',
    )
    def put(self, **kwargs):
        releases_order: dict = kwargs['releases']  # '<order>': '<track_id>'

        release_ctl = get_release_ctl()
        release_list_entity = release_ctl.change_order(releases_order)

        return {
            "status": "Success",
            "releases": ReleaseListScheme.from_entity(release_list_entity)['releases']
        }
