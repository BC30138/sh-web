import os
from shweb import APP_PATH


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
    AWS_CLOUD_FRONT_ID = os.environ.get('AWS_CLOUD_FRONT_ID')

    SEND_FILE_MAX_AGE_DEFAULT = 0
    BABEL_DEFAULT_LOCALE = 'en'
    LANGUAGES = {
        'en': "English",
        'ru': "Russian"
    }
    TEMPLATES_PATH = str(
        APP_PATH.parent.joinpath(
            'services'
        ).joinpath(
            'rest'
        ).joinpath(
            'templates'
        ).absolute()
    )
    STATIC_PATH = str(
        APP_PATH.parent.joinpath(
            'services'
        ).joinpath(
            'rest'
        ).joinpath(
            'static'
        ).absolute()
    )
