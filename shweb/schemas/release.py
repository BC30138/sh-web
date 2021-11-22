import requests
from ast import literal_eval
from marshmallow import Schema, fields, pre_load, post_dump, validate
from bs4 import BeautifulSoup

from shweb.utils import get_release_types, get_month_name


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
    release_name = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(["Single", "Album", "EP"]))
    release_id = fields.Str(required=True)
    bandcamp_id = fields.Str(required=False)
    bandcamp_link = fields.Str(required=False)
    date = fields.Str(required=True)
    default_open_text = fields.Str(required=False, allow_none=True)
    services = fields.List(fields.Nested(ServiceSchema), required=True)
    tracklist = fields.List(fields.Nested(TrackSchema), required=True)
    youtube_videos = fields.List(fields.Str, required=False)

    @pre_load
    def add_bandcamp_type(self, in_data, **kwargs):
        if "bandcamp_id" not in in_data:
            response = requests.get(in_data['bandcamp_link'])
            soup = BeautifulSoup(response.text, "html.parser")
            in_data['bandcamp_id'] = str(literal_eval(
                soup.head.find("meta", {"name": "bc-page-properties"})['content']
            )['item_id'])

        if in_data['type'] == "Single":
            bandcamp_type = "track"
        elif in_data['type'] == "Album":
            bandcamp_type = "album"
        in_data['bandcamp_id'] = f"{bandcamp_type}={in_data['bandcamp_id']}"
        return in_data

    @post_dump
    def language_update(self, data, **kwargs):
        date_month = data['date'].split()[1]
        data['date'] = data['date'].replace(date_month, get_month_name()[date_month])

        data['type'] = get_release_types()[data['type']]
        return data
