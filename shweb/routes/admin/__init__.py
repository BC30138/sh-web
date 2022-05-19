from flask import Blueprint  # type: ignore
from flask_restful import Api  # type: ignore
from shweb.routes.admin.auth import get_user_info_from_token
from shweb.routes.admin.routes import login, admin_index, admin_release, edit_home


blueprint = Blueprint("admin", __name__)
api = Api(blueprint)
api.add_resource(admin_index.IndexResource, "/", endpoint="index")
api.add_resource(login.LoginResource, "/login", endpoint="login")
api.add_resource(login.LogoutResource, "/logout", endpoint="logout")
api.add_resource(login.ForgetResource, "/login/forget", endpoint="forget")
api.add_resource(login.ForgetConfirmResource, "/login/forget/confirm", endpoint="forget-confirm")
api.add_resource(login.ChangePasswordResource, "/login/change-password", endpoint="change-password")
api.add_resource(admin_release.ReleaseResource, "/release", endpoint="release")
api.add_resource(edit_home.EditHomeResource, "/index-edit", endpoint="edit-home")
api.add_resource(edit_home.PreviewResource, "/index-edit/preview", endpoint="edit-home-preview")


@blueprint.context_processor
def utility_processor():
    return dict(
        get_user_info_from_token=get_user_info_from_token
    )
