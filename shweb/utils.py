import json
import requests
from time import time

from flask import current_app
from flask_babel import _
import boto3


def get_release_types():
    return {
        'Single': _('Single'),
        'Album': _('Album'),
        'Ep': _('Ep'),
        'single': _('single'),
        'album': _('album'),
        'ep': _('ep')
    }


def get_month_name():
    return {
        'jan': _('jan'),
        'feb': _('feb'),
        'mar': _('mar'),
        'apr': _('apr'),
        'may': _('may'),
        'jun': _('jun'),
        'jul': _('jul'),
        'aug': _('aug'),
        'sep': _('sep'),
        'oct': _('oct'),
        'nov': _('nov'),
        'dec': _('dec')
    }


def get_release_list():
    base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
    response = requests.get(f"{base}/releases/release-list.json")
    releases: list = response.json()['releases']
    releases = list(map(
        lambda x: x.update({'lang_type': get_release_types()[x['type']]}) or x,
        releases
    ))
    return releases


def upload_json(json_data, file_path):
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
    )

    s3_object = s3_resource.Object(current_app.config['S3_BUCKET_NAME'], file_path)
    s3_object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )


def create_invalidation(items):
    client = boto3.client(
        'cloudfront',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
    )
    client.create_invalidation(
        DistributionId=current_app.config['AWS_CLOUD_FRONT_ID'],
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': items,
            },
            'CallerReference': str(time()).replace(".", "")
        }
    )
