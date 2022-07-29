from flask import Flask
# from shweb.services.rest.routes import admin
from shweb.services.rest.routes.public import index, releases, feed


def register_blueprints(app: Flask):
    app.register_blueprint(index.blueprint, url_prefix="/")
    app.register_blueprint(releases.blueprint, url_prefix="/releases")
    app.register_blueprint(feed.blueprint, url_prefix="/feed")
    # app.register_blueprint(admin.blueprint, url_prefix="/admin")
