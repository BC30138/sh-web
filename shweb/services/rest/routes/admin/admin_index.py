import requests

from flask import render_template, make_response, current_app
from flask_restful import Resource, reqparse, abort, request

from shweb.services.rest.rest_helpers.common import auth_required
from shweb.utils import upload_json, create_invalidation


release_list_order_parser = reqparse.RequestParser()
release_list_order_parser.add_argument("releases", location="json", required=True)


class IndexResource(Resource):
    template = 'admin/index.html'
    @auth_required
    def get(self):
        return make_response(render_template(self.template))

    @auth_required
    def put(self):
        json_data = request.get_json()
        releases = json_data.get('releases')
        if releases is None:
            return abort(400)

        release_list_fp = "releases/release-list.json"

        base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
        response = requests.get(f"{base}/{release_list_fp}")
        s3_releases: list = response.json()['releases']

        new_s3_releases = []
        for key in sorted(releases):
            release = next(item for item in s3_releases if item["id"] == releases[key])
            new_s3_releases.append(release)

        upload_json({"releases": new_s3_releases}, release_list_fp)
        create_invalidation(["/" + release_list_fp])
        return {
            "status": "Success",
            "releases": new_s3_releases
        }
