import json
import requests
from time import time

from flask import current_app
import boto3

from shweb.services.rest.schemas.release_list import ReleaseListSchema


def get_raw_release_list():
    base = current_app.config['AWS_CLOUD_FRONT_DOMAIN']
    return requests.get(f"{base}/releases/release-list.json").json()


def get_release_list():
    response = get_raw_release_list()
    schema = ReleaseListSchema()
    schema_deserial = schema.load(response)
    return schema.dump(schema_deserial)


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


def upload_file(file, file_path):
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
    )
    s3_object = s3_resource.Object(current_app.config['S3_BUCKET_NAME'], file_path)
    s3_object.put(
        Body=file.read()
    )


def s3_delete(prefix):
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
    )
    bucket = s3_resource.Bucket(current_app.config['S3_BUCKET_NAME'])
    bucket.objects.filter(Prefix=prefix).delete()


def create_invalidation(items):
    client = boto3.client(
        'cloudfront',
        region_name=current_app.config['AWS_REGION'],
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
