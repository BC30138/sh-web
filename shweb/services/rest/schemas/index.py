"""Схемы для rest-коммуникаций с индексом"""

import re
import ast
from typing import Optional

from marshmallow import Schema, fields, pre_load
from flask_babel import get_locale

from shweb.ctx.index.model import ClientIndexEntity, IndexEntity
from shweb.config import Config


def parse_variables(code: str, images: Optional[dict] = None):
    if images is None:
        images = {}
    def match_func(match):
        var: str = match.group()[2:-2]
        var = var.strip()
        if var == "lang_arg":
            value = f"?lang={get_locale()}"
        else:
            action, value = var.split("=", 1)
            action = action.strip()
            value = value.strip()
            if action == "image":
                if value in images:
                    value = images[value]
                else:
                    value = f"{Config.AWS_CLOUD_FRONT_DOMAIN}/index/files/{value}"
            if action == "translate":
                lang = str(get_locale())
                value = ast.literal_eval(value)[lang]
        return value
    return re.sub(r"({){2,}.*?(}){2,}", match_func, code, re.DOTALL)


class ClientIndexScheme(Schema):
    style = fields.Str(required=True)
    content = fields.Str(required=True)

    @classmethod
    def from_entity(cls, client_index_entity: ClientIndexEntity, images: Optional[dict] = None) -> dict:
        return cls().load(dict(
            style=f"<style>{client_index_entity.style}</style>",
            content=parse_variables(code=client_index_entity.content, images=images),
        ))


class IndexScheme(Schema):
    client_index = fields.Dict(required=True)
    files_list = fields.List(fields.Str, Required=False, allow_none=True)

    @classmethod
    def from_entity(
        cls,
        index_entity: IndexEntity,
        is_mobile: bool = False,
    ) -> dict:
        if is_mobile:
            client_index = ClientIndexScheme.from_entity(index_entity.mobile)
        else:
            client_index = ClientIndexScheme.from_entity(index_entity.web)
        return cls().load(dict(
            client_index=client_index,
            files_list=index_entity.files_list,
        ))


class IndexRawScheme(Schema):
    web = fields.Dict(required=True)
    mobile = fields.Dict(required=True)
    files_list = fields.List(fields.Str, Required=False, allow_none=True)

    @pre_load()
    def to_dict(self, item, **kwargs):
        if isinstance(item, str):
            return ast.literal_eval(item)
        return item

    @classmethod
    def from_entity(cls, index_entity: IndexEntity) -> dict:
        return cls().load(dict(
            web=ClientIndexScheme.from_entity(index_entity.web),
            mobile=ClientIndexScheme.from_entity(index_entity.mobile),
            files_list=index_entity.files_list,
        ))


class IndexAdminScheme(IndexRawScheme):
    files = fields.List(fields.List(fields.Str), Required=False)

    @classmethod
    def from_entity(cls, index_entity: IndexEntity) -> dict:
        raw = super().from_entity(index_entity)
        files = []
        if index_entity.files_list is not None:
            files = [
                [file_name, f"{Config.AWS_CLOUD_FRONT_DOMAIN}/index/files/{file_name}"]
                for file_name in index_entity.files_list
            ]
        return cls().load(dict(
            files=files,
            **raw,
        ))
