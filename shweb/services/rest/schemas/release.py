import json
import requests
from ast import literal_eval
from marshmallow import Schema, fields, pre_load, post_dump, validate
from marshmallow.exceptions import ValidationError
from bs4 import BeautifulSoup

from shweb.services.rest.translate_helpers import get_release_types, get_month_names


class ServiceSchema(Schema):
    name = fields.Str(required=True)
    link = fields.Url()


class TrackSchema(Schema):
    name = fields.Str(required=True)
    id = fields.Str(required=True)
    written = fields.Str(required=False)
    lyrics = fields.Str(required=False)
    explicit = fields.Bool(required=False)


class ReleaseSchema(Schema):
    release_id = fields.Str(required=True)
    release_name = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(["Single", "Album", "EP"]))
    bandcamp_id = fields.Str(required=False)
    bandcamp_link = fields.Str(required=False)
    date = fields.Str(required=True)
    default_open_text = fields.Str(required=False, allow_none=True)
    services = fields.List(fields.Nested(ServiceSchema), required=True)
    tracklist = fields.List(fields.Nested(TrackSchema), required=True)
    youtube_videos = fields.List(fields.Str, required=False)

    @pre_load
    def pre_load_func(self, in_data, **kwargs):
        try:
            if "bandcamp_id" not in in_data:
                response = requests.get(in_data['bandcamp_link'])
                soup = BeautifulSoup(response.text, "html.parser")
                in_data['bandcamp_id'] = str(literal_eval(
                    soup.head.find("meta", {"name": "bc-page-properties"})['content']
                )['item_id'])
        except Exception:
            raise ValidationError("bad bandcamp link")

        is_bandcamp_service = False
        for object in in_data['services']:  # for name, age in dictionary.iteritems():  (for Python 2.x)
            if object['name'] == "bandcamp":
                is_bandcamp_service = True

        if not is_bandcamp_service:
            in_data['services'].append({
                "name": "bandcamp",
                "link": in_data['bandcamp_link']
            })

        return in_data

    @post_dump
    def post_dump_function(self, data, **kwargs):
        if data['type'] == "Single":
            bandcamp_type = "track"
        elif data['type'] == "Album":
            bandcamp_type = "album"

        data['bandcamp_id'] = f"{bandcamp_type}={data['bandcamp_id']}"

        year, month, day = data['date'].split('-')

        data['date'] = f"{day} {get_month_names()[int(month) - 1]} {year}"

        data['type'] = get_release_types()[data['type']]

        return data


class EditReleaseSchema(ReleaseSchema):
    @post_dump
    def post_dump_function(self, data, **kwargs):
        for service in data['services']:
            if service['name'] != "bandcamp":
                data[f"service_{service['name']}"] = service['link']
        if 'youtube_videos' in data:
            data['youtube_videos'] = [f"https://youtu.be/{yid}" for yid in data['youtube_videos']]

        data['tracklist'] = json.dumps(data['tracklist'])
        return data
