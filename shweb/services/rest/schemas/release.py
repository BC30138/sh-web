import json

from marshmallow import Schema, fields, post_dump

from shweb.ctx.release.model import ReleaseEntity, TrackEntity, ServiceEntity
from shweb.services.rest.translate_helpers import compile_release_type, get_month_names
from shweb.util.enums import ReleaseType


class ServiceScheme(Schema):
    name = fields.Str(required=True)
    link = fields.Url()

    @classmethod
    def from_entity(cls, service_entity: ServiceEntity):
        return cls().load(dict(
            name=service_entity.name,
            link=service_entity.link,
        ))


class TrackScheme(Schema):
    name = fields.Str(required=True)
    track_id = fields.Str(required=True)
    written = fields.Str(required=False, allow_none=True)
    lyrics = fields.Str(required=False, allow_none=True)
    explicit = fields.Bool(required=False, allow_none=True)

    @classmethod
    def from_entity(cls, track_entity: TrackEntity):
        return cls().load(dict(
            name=track_entity.name,
            track_id=track_entity.track_id,
            written=track_entity.written,
            lyrics=track_entity.lyrics,
            explicit=track_entity.explicit,
        ))


class ReleaseScheme(Schema):
    release_id = fields.Str(required=True)
    release_name = fields.Str(required=True)
    release_type = fields.Str(required=True)
    bandcamp_id = fields.Str(required=False, allow_none=True)
    bandcamp_link = fields.Str(required=False, allow_none=True)
    release_date = fields.Str(required=True)
    default_open_text = fields.Str(required=False, allow_none=True)
    services = fields.List(fields.Dict, required=True)
    tracklist = fields.List(fields.Dict, required=True)
    youtube_videos = fields.List(fields.Str, required=False, allow_none=True)

    @classmethod
    def from_entity(cls, release_entity: ReleaseEntity):
        if release_entity.release_type == ReleaseType.SINGLE:
            bandcamp_type = 'track'
        else:
            bandcamp_type = 'album'
        bandcamp_id = f'{bandcamp_type}={release_entity.bandcamp_id}'

        if release_entity.release_date is None:
            raise ValueError('Release date must be initialized')
        day = release_entity.release_date.day
        month = get_month_names()[int(release_entity.release_date.month) - 1]
        year = release_entity.release_date.year
        date_str = f'{day} {month} {year}'

        return cls().load(dict(
            release_id=release_entity.release_id,
            release_name=release_entity.release_name,
            release_type=compile_release_type(release_entity.release_type),
            services=[ServiceScheme.from_entity(service_entity) for service_entity in release_entity.services],
            tracklist=[TrackScheme.from_entity(track_entity) for track_entity in release_entity.tracklist],
            bandcamp_id=bandcamp_id,
            bandcamp_link=release_entity.bandcamp_link,
            release_date=date_str,
            default_open_text=release_entity.default_open_text,
            youtube_videos=release_entity.youtube_videos if release_entity.youtube_videos else [],
        ))


class EditReleaseSchema(ReleaseScheme):
    @post_dump
    def post_dump_function(self, data, **kwargs):
        for service in data['services']:
            if service['name'] != "bandcamp":
                data[f"service_{service['name']}"] = service['link']
        if 'youtube_videos' in data:
            data['youtube_videos'] = [f"https://youtu.be/{yid}" for yid in data['youtube_videos']]

        data['tracklist'] = json.dumps(data['tracklist'])
        return data
