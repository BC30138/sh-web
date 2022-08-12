"""Страница для изменения индекса"""

import ast
import enum
from typing import List, Tuple

from flask import render_template, make_response
from flask_restful import Resource, output_json
from flask_apispec import use_kwargs
from marshmallow import Schema, fields, pre_load
from marshmallow_enum import EnumField
from werkzeug.datastructures import FileStorage

from shweb.ctx.index.model import IndexEntity, ClientIndexEntity
from shweb.extensions.rest.rest_helpers.common import auth_required
from shweb.extensions.rest.rest_helpers.getters import get_index_ctl
from shweb.extensions.rest.schemas.index import IndexAdminScheme, IndexRawScheme, ClientIndexScheme


class DeviceType(enum.Enum):
    WEB = 'web'
    MOBILE = 'mobile'


class InputDeleteScheme(Schema):
    delete = fields.List(fields.Str, required=False, missing=None)

    @pre_load
    def to_list(self, item, **kwargs):
        return {'delete': ast.literal_eval(item['delete'][0])}


class EditHomeResource(Resource):
    template = "admin/edit_home.html"

    @auth_required
    def get(self):
        index_clt = get_index_ctl()
        index_entity = index_clt.get()

        index_code = IndexAdminScheme.from_entity(index_entity)
        return make_response(render_template(self.template, index_code=index_code))

    @auth_required
    @use_kwargs({
        'index_code': fields.Nested(IndexRawScheme, required=True),
    }, location='form')
    @use_kwargs(InputDeleteScheme, location='form')
    @use_kwargs({
        'files': fields.Field(required=False, missing={}),
    }, location="request-files")
    def put(
        self,
        index_code: dict,
        delete: List[str],
        files: List[Tuple[str, FileStorage]],
    ):
        index_ctl = get_index_ctl()

        index_entity = IndexEntity(
            web=ClientIndexEntity(
                style=index_code['web']['style'],
                content=index_code['web']['content'],
            ),
            mobile=ClientIndexEntity(
                style=index_code['mobile']['style'],
                content=index_code['mobile']['content'],
            ),
            files_list=index_code['files_list'],
        )

        index_ctl.upload(
            index_entity=index_entity,
            to_delete=delete,
            files=files,
        )
        return output_json({'status': "ok"}, 200)


class PreviewResource(Resource):
    @auth_required
    @use_kwargs({
        'index_code': fields.Dict(
            keys=fields.Str,
            values=fields.Str,
            required=True,
        ),
        'images': fields.Dict(
            keys=fields.Str,
            values=fields.Str,
            required=True,
        ),
    }, location='json')
    @use_kwargs({
        'device': EnumField(DeviceType, by_value=True, required=True)
    }, location='query')
    def post(
        self,
        index_code: dict,
        images: dict,
        device: DeviceType,
    ):
        index_entity = ClientIndexEntity(
            style=index_code['style'],
            content=index_code['content'],
        )

        if device == DeviceType.MOBILE:
            template = "public/mobile/index.html"
        elif device == DeviceType.WEB:
            template = "public/web/index.html"
        else:
            return make_response({'error': 'device type is not implemented'}, 500)

        index_response = ClientIndexScheme.from_entity(
            client_index_entity=index_entity,
            images=images,
        )
        return make_response(
            render_template(
                template,
                style_code=index_response['style'],
                content_code=index_response['content']
            )
        )
