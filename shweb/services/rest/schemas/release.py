import json
from typing import List, Optional

from marshmallow import Schema, fields, post_dump, validate

from pydantic import BaseModel

from shweb.ctx.release.model import ReleaseEntity, TrackEntity, ServiceEntity
from shweb.services.rest.translate_helpers import get_release_types, get_month_names
from shweb.util.enums import ReleaseType


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

    # @post_dump
    # def post_dump_function(self, data, **kwargs):
    #     if data['type'] == "Single":
    #         bandcamp_type = "track"
    #     elif data['type'] == "Album":
    #         bandcamp_type = "album"
    #
    #     data['bandcamp_id'] = f"{bandcamp_type}={data['bandcamp_id']}"
    #
    #     year, month, day = data['date'].split('-')
    #
    #     data['date'] = f"{day} {get_month_names()[int(month) - 1]} {year}"
    #
    #     data['type'] = get_release_types()[data['type']]
    #
    #     return data


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


class ServiceScheme(BaseModel):
    name: str
    link: str

    @classmethod
    def from_entity(cls, service_entity: ServiceEntity):
        return cls(
            name=service_entity.name,
            link=service_entity.link,
        )


class TrackScheme(BaseModel):
    name: str
    track_id: str
    written: Optional[str]
    lyrics: Optional[str]
    explicit: Optional[bool]

    @classmethod
    def from_entity(cls, track_entity: TrackEntity):
        return cls(
            name=track_entity.name,
            track_id=track_entity.track_id,
            written=track_entity.written,
            lyrics=track_entity.lyrics,
            explicit=track_entity.explicit,
        )


class ReleaseScheme(BaseModel):
    release_id: str
    release_name: str
    release_type: ReleaseType
    services: List[ServiceScheme]
    tracklist: List[TrackScheme]
    bandcamp_id: Optional[str]
    bandcamp_link: Optional[str]
    release_date: Optional[str]
    default_open_text: Optional[str]
    youtube_videos: Optional[List[str]]

    @classmethod
    def from_entity(cls, release_entity: ReleaseEntity):
        if release_entity.release_type == ReleaseType.SINGLE:
            bandcamp_type = 'track'
        else:
            bandcamp_type = 'album'
        bandcamp_id = f'{bandcamp_type}={release_entity.bandcamp_id}'

        day = release_entity.release_date.day
        month = get_month_names()[int(release_entity.release_date.month) - 1]
        year = release_entity.release_date.year
        date_str = f'{day} {month} {year}'

        return cls(
            release_id=release_entity.release_id,
            release_name=release_entity.release_name,
            release_type=release_entity.release_type,
            services=[ServiceScheme.from_entity(service_entity) for service_entity in release_entity.services],
            tracklist=[TrackScheme.from_entity(track_entity) for track_entity in release_entity.tracklist],
            bandcamp_id=bandcamp_id,
            bandcamp_link=release_entity.bandcamp_link,
            release_date=date_str,
            default_open_text=release_entity.default_open_text,
            youtube_videos=release_entity.youtube_videos,
        )
