from flask import Blueprint

from warrant import Cognito
import botocore.exceptions

import boto3

blueprint = Blueprint("admin", __name__)

from shweb.routes.admin.routes import index, login
from shweb.routes.admin.auth import get_user_info_from_token


@blueprint.context_processor
def utility_processor():
    return dict(
        get_user_info_from_token=get_user_info_from_token
    )
