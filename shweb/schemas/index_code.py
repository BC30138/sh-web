import re
import ast

from marshmallow import Schema, fields, pre_load, post_dump
from flask import current_app
from flask_babel import get_locale


def replace_action_parser(match):
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


def parse_variables(code: str):
    return re.sub(r"({){2,}.*?(}){2,}", replace_action_parser, code, re.DOTALL)


class DeviceCode(Schema):
    style = fields.Str(required=True)
    content = fields.Str(required=True)

    @post_dump
    def post_dump_function(self, data, **kwargs):
        data['style'] = f"<style>{data['style']}</style>"
        data['content'] = parse_variables(data['content'])
        if 'files_list' in data:
            data['files_list'] = [[f"{item}", "cloud"] for item in data['files_list']]
        return data


class IndexCode(Schema):
    web = fields.Nested(DeviceCode, required=True)
    mobile = fields.Nested(DeviceCode, required=True)
    files_list = fields.List(fields.Str, Required=False)