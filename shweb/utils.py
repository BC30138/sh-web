import os
from re import M
from flask.app import Flask
from flask_babel import _
from flask import Flask
import boto3


def download_directory_s3(bucket, remote_path, output_path,
                          aws_access_key_id, aws_secret_access_key):
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    bucket = s3_resource.Bucket(bucket)
    for obj in bucket.objects.filter(Prefix=remote_path):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key)


def load_releases(app: Flask):
    download_directory_s3(
        "stanethuzhe-web",
        "releases",
        app.config['AWS_ACCESS_KEY'],
        app.config['AWS_SECRET_KEY']
    )


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
