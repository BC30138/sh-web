from flask import Blueprint

from warrant import Cognito
import botocore.exceptions

import boto3

blueprint = Blueprint("admin", __name__)

from shweb.routes.admin.routes import index, login
