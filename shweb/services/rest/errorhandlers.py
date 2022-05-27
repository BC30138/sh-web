from flask import Flask
from flask.templating import render_template
from jinja2.exceptions import TemplateNotFound

from shweb.services.rest.rest_helpers import mobile_template


@mobile_template(['public'], 'error.html')
def page_not_found(_exc, template):
    return render_template(template, message="404 not found :(")


@mobile_template(['public'], 'error.html')
def template_not_found(_exc, template):
    return render_template(template, message="404 not found :(")


@mobile_template(['public'], 'error.html')
def server_error(_exc, template):
    return render_template(template, message="500 server error :(")


@mobile_template(['public'], 'error.html')
def unprocessable_error(_exc, template):
    return render_template(template, message="422 bad request :(")


def register_errorhandlers(app: Flask):
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(TemplateNotFound, template_not_found)
    app.register_error_handler(422, unprocessable_error)
    # app.register_error_handler(Exception, server_error)
