import requests
import re
import ast
from flask import Blueprint, render_template, current_app
from flask import _request_ctx_stack as stack
from flask_mobility.decorators import mobile_template
from flask_babel import get_locale

blueprint = Blueprint("index-page", __name__)


style_tags = {
    "start": r"{%style%}",
    "end": r"{%style-end%}",
    "start-mobile": r"{%style-mobile%}",
    "end-mobile": r"{%style-mobile-end%}",
}

content_tags = {
    "start": r"{%content%}",
    "end": r"{%content-end%}",
    "start-mobile": r"{%content-mobile%}",
    "end-mobile": r"{%content-mobile-end%}"
}


def mobile_checker():
    ctx = stack.top
    is_mobile = False
    if ctx is not None and hasattr(ctx, "request"):
        request = ctx.request
        is_mobile = getattr(request, "MOBILE", False)
    return is_mobile


def find_code(tags, text, is_mobile) -> str:
    if is_mobile:
        start_key = "start-mobile"
        end_key = "end-mobile"
    else:
        start_key = "start"
        end_key = "end"
    regex_result = re.findall(
        f"{tags[start_key]}.*?{tags[end_key]}",
        text,
        re.DOTALL
    )
    if regex_result:
        return regex_result[0][len(tags[start_key]):-len(tags[end_key])]
    else:
        return re.findall(
            f"{tags['start']}.*?{tags['end']}",
            text,
            re.DOTALL
        )[0][len(tags['start']):-len(tags['end'])]


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
            value = f"{current_app.config['AWS_CLOUD_FRONT_DOMAIN']}/index/{value}"
        if action == "translate":
            lang = str(get_locale())
            value = ast.literal_eval(value)[lang]
    return value


def parse_variables(code: str):
    return re.sub(r"({){2,}.*?(}){2,}", replace_action_parser, code, re.DOTALL)


@blueprint.route('/')
@blueprint.route('/index')
@mobile_template('{mobile/}index.html')
def index(template):
    base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
    index_code = requests.get(f"{base}/index/index.code").text
    index_code = re.sub(
        r"{%.*?%}",
        lambda x: r"{%" + x.group()[2:-2].strip() + r"%}",
        index_code,
        re.DOTALL
    )
    is_mobile = mobile_checker()
    style_code = f"<style>{find_code(style_tags, index_code, is_mobile)}</style>"
    content_code = find_code(content_tags, index_code, is_mobile)
    content_code = parse_variables(content_code)
    return render_template(template, title='Home', style_code=style_code, content_code=content_code)
