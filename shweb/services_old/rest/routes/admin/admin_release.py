"""Страница редактирования/создания релиза"""

import enum
import logging
from typing import Optional

from flask import redirect, url_for, render_template, make_response
from marshmallow_enum import EnumField
from flask_restful import Resource
from flask_apispec import use_kwargs
from webargs import fields
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound

from shweb.ctx.release.model import ReleaseEntity, ReleaseListItemEntity
from shweb.extensions.rest.rest_helpers.common import auth_required
from shweb.extensions.rest.rest_helpers.getters import get_release_ctl
from shweb.extensions.rest.schemas.release import ReleaseScheme


class ActionType(enum.Enum):
    CREATE_NEW = 'new'
    EDIT_EXIST = 'edit'


release_id_scheme = fields.Str(required=False, missing=None)


class ReleaseResource(Resource):
    template = 'admin/release.html'

    @auth_required
    @use_kwargs({
        'action': EnumField(ActionType, by_value=True, required=True),
        'id': release_id_scheme,
    }, location='query')
    def get(
            self,
            action: ActionType,
            id: Optional[str],
    ):
        release = {}
        if action == ActionType.EDIT_EXIST:
            if id is None:
                return redirect(url_for('admin.release', action=ActionType.CREATE_NEW.value))

            release_ctl = get_release_ctl()
            release_entity = release_ctl.get(
                release_id=id,
            )
            if release_entity is None:
                logging.info('release entity not found')
                raise NotFound('Release entity not found')
            release = ReleaseScheme.from_entity(
                release_entity=release_entity,
                edit_scheme=True,
            )

        return make_response(
            render_template(
                self.template,
                action=action.value,
                release=release
            )
        )

    # TODO: можно сделать одним методом с обновлением
    @auth_required
    @use_kwargs({
        'release': fields.Nested(ReleaseScheme, required=True),
    }, location='form')
    @use_kwargs({
        'cover': fields.Field(
            required=False,
            validate=lambda file: file.mimetype == 'image/jpeg',
            missing=None,
        ),
        'og': fields.Field(
            required=False,
            validate=lambda file: file.mimetype == 'image/jpeg',
            missing=None,
        ),
    }, location='files')
    def post(
        self,
        release,
        cover,
        og,
    ):
        release_entity = ReleaseEntity.from_dict(release)

        release_ctl = get_release_ctl()

        new_release = ReleaseListItemEntity(
            release_id=release_entity.release_id,
            release_name=release_entity.release_name,
            release_type=release_entity.release_type,
        )
        release_ctl.upsert_release_list_item(
            new_release=new_release,
        )
        release_ctl.upload_release_objects(
            release_entity=release_entity,
            cover=cover,
            og=og,
        )
        return make_response({'status': "ok"}, 200)

    @auth_required
    @use_kwargs({'id': release_id_scheme}, location='query')
    @use_kwargs({
        'release': fields.Nested(ReleaseScheme, required=True),
    }, location='form')
    @use_kwargs({
        'cover': fields.Field(
            required=False,
            validate=lambda file: file.mimetype == 'image/jpeg',
            missing=None,
        ),
        'og': fields.Field(
            required=False,
            validate=lambda file: file.mimetype == 'image/jpeg',
            missing=None,
        ),
    }, location='files')
    def put(
        self,
        id: str,
        release: dict,
        cover: Optional[FileStorage],
        og: Optional[FileStorage],
    ):
        release_entity = ReleaseEntity.from_dict(release)

        release_ctl = get_release_ctl()

        new_release = ReleaseListItemEntity(
            release_id=release_entity.release_id,
            release_name=release_entity.release_name,
            release_type=release_entity.release_type,
        )
        release_ctl.upsert_release_list_item(
            release_id=id,
            new_release=new_release,
        )
        release_ctl.upload_release_objects(
            release_entity=release_entity,
            cover=cover,
            og=og,
        )
        return make_response({'status': "ok"}, 200)

    @auth_required
    @use_kwargs({'id': release_id_scheme}, location='query')
    def delete(self, id: str):
        release_ctl = get_release_ctl()
        release_ctl.remove_release(id)
        return make_response({'status': "ok"}, 200)
