import os
import pathlib

from flask.cli import load_dotenv
import boto3

CONFIG_PATH = pathlib.Path(__file__)
load_dotenv(str(CONFIG_PATH.parent.parent.joinpath('.env').absolute()))


def get_cloudfront_id():
    domain_name = os.environ.get('AWS_CLOUD_FRONT_DOMAIN').split("https://")[1]
    client = boto3.client(
        'cloudfront',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    )
    distributions = client.list_distributions()['DistributionList']['Items']
    for item in distributions:
        if item['DomainName'] == domain_name:
            return item['Id']


class Config:
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    AWS_REGION = os.environ.get('AWS_REGION')

    COGNITO_REGION = os.environ.get('AWS_REGION')
    COGNITO_USERPOOL_ID = os.environ.get('AWS_USER_POOL_ID')
    COGNITO_APP_CLIENT_ID = os.environ.get('AWS_APP_CLIENT_ID')
    COGNITO_APP_CLIENT_SECRET = os.environ.get('AWS_APP_CLIENT_SECRET')
    COGNITO_JWKS_KEYS_URL = f"https://cognito-idp.{os.environ.get('AWS_REGION')}.amazonaws.com/" + \
                            f"{os.environ.get('AWS_USER_POOL_ID')}/.well-known/jwks.json"

    AWS_CLOUD_FRONT_DOMAIN = os.environ.get('AWS_CLOUD_FRONT_DOMAIN')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    AWS_CLOUD_FRONT_ID = get_cloudfront_id()

    SEND_FILE_MAX_AGE_DEFAULT = 0
    BABEL_DEFAULT_LOCALE = 'en'
    LANGUAGES = {
        'en': "English",
        'ru': "Russian"
    }
    TEMPLATES_PATH = str(CONFIG_PATH.parent.joinpath('templates').absolute())
    STATIC_PATH = str(CONFIG_PATH.parent.joinpath('static').absolute())
