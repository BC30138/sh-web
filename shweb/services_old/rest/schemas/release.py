"""Схемы для rest-коммуникаций с релизами"""

import json

from marshmallow import Schema, fields, pre_load

from shweb.ctx.release.model import ReleaseEntity, TrackEntity, ServiceEntity, ReleaseListEntity, ReleaseListItemEntity
from shweb.util.enums import ReleaseType
from shweb.extensions.rest.rest_helpers.translate import compile_release_type, get_month_names


class ServiceScheme(Schema):
    name = fields.Str(required=True)
    link = fields.Url()

    @classmethod
    def from_entity(cls, service_entity: ServiceEntity) -> dict:
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
    def from_entity(cls, track_entity: TrackEntity) -> dict:
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

    @pre_load()
    def to_dict(self, item, **kwargs):
        if isinstance(item, str):
            return json.loads(item)
        return item

    @classmethod
    def from_entity(cls, release_entity: ReleaseEntity, edit_scheme: bool = False) -> dict:
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

        data = cls().load(dict(
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

        if edit_scheme:
            data['youtube_videos'] = [
                f'https://youtu.be/{yid}' for yid in release_entity.youtube_videos
            ] if release_entity.youtube_videos else []

            for service in release_entity.services:
                data[f'service_{service.name}'] = service.link

            data['tracklist'] = json.dumps(data['tracklist'])
            data['release_date'] = release_entity.release_date.isoformat()

        return data


class ReleaseListItemScheme(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    lang_type = fields.Str(required=True)

    @classmethod
    def from_entity(
        cls,
        release_list_item_entity: ReleaseListItemEntity,
        type_upper: bool = False,
    ) -> dict:
        return cls().load(dict(
            id=release_list_item_entity.release_id,
            type=release_list_item_entity.release_type.value,
            lang_type=compile_release_type(release_list_item_entity.release_type, type_upper),
            name=release_list_item_entity.release_name,
        ))


class ReleaseListScheme(Schema):
    releases = fields.List(fields.Dict, required=True)

    @classmethod
    def from_entity(
            cls,
            release_list_entity: ReleaseListEntity,
    ) -> dict:
        return cls().load(dict(
            releases=[ReleaseListItemScheme.from_entity(item_entity) for item_entity in release_list_entity.releases]
        ))
