"""Схемы для rest-коммуникаций с индексом"""

import re
import ast

from marshmallow import Schema, fields
from flask import current_app
from flask_babel import get_locale

from shweb.ctx.index.model import ClientIndexEntity, IndexEntity
from shweb.services.rest.rest_helpers import mobile_checker

def parse_variables(code: str):
    def f(match):
        var: str = match.group()[2:-2]
        var = var.strip()
        if var == "lang_arg":
            value = f"?lang={get_locale()}"
        else:
            action, value = var.split("=", 1)
            action = action.strip()
            value = value.strip()
            if action == "image":
                value = f"{current_app.config['AWS_CLOUD_FRONT_DOMAIN']}/index/files/{value}"
            if action == "translate":
                lang = str(get_locale())
                value = ast.literal_eval(value)[lang]
        return value
    return re.sub(r"({){2,}.*?(}){2,}", f, code, re.DOTALL)


class ClientIndexScheme(Schema):
    style = fields.Str(required=True)
    content = fields.Str(required=True)

    @classmethod
    def from_entity(cls, client_index_entity: ClientIndexEntity) -> dict:
        return cls().load(dict(
            style=f"<style>{client_index_entity.style}</style>",
            content=parse_variables(client_index_entity.content),
        ))


class IndexScheme(Schema):
    client_index = fields.Dict(required=True)
    files_list = fields.List(fields.Str, Required=False, allow_none=True)

    @classmethod
    def from_entity(cls, index_entity: IndexEntity) -> dict:
        if mobile_checker():
            client_index = ClientIndexScheme.from_entity(index_entity.mobile)
        else:
            client_index = ClientIndexScheme.from_entity(index_entity.web)
        return cls().load(dict(
            client_index=client_index,
            files_list=index_entity.files_list,
        ))
