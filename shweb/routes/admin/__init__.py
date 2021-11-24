from flask import Blueprint
from flask_restful import Api
from shweb.routes.admin.auth import get_user_info_from_token
from shweb.routes.admin.routes import login, index, release


blueprint = Blueprint("admin", __name__)
api = Api(blueprint)
api.add_resource(index.IndexResource, "/", endpoint="index")
api.add_resource(login.LoginResource, "/login", endpoint="login")
api.add_resource(login.ForgetResource, "/login/forget", endpoint="forget")
api.add_resource(login.ForgetConfirmResource, "/login/forget/confirm", endpoint="forget-confirm")
api.add_resource(login.ChangePasswordResource, "/login/change-password", endpoint="change-password")
api.add_resource(release.ReleaseResource, "/release", endpoint="release")


@blueprint.context_processor
def utility_processor():
    return dict(
        get_user_info_from_token=get_user_info_from_token
    )
