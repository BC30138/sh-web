"""Сервис для получения данных из хранилища"""

import logging
from typing import List
from time import time
import requests
import json

import boto3
from botocore.client import BaseClient
from werkzeug.datastructures import FileStorage

from shweb.config import Config


class Error(Exception):
    pass


class ObjectStorageAPI:
    def __init__(
        self,
        cloud_front_base: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str,
        cdn_id: str,
    ):
        self._cloud_front_base = cloud_front_base
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket_name = bucket_name
        self._region = region
        self._cdn_id = cdn_id

    def get(
        self,
        path: str,
    ) -> dict:
        response = requests.get(f"{self._cloud_front_base}/{path}")
        logging.info(f'GET {response.url} {response.status_code}')
        if response.status_code != 200:
            logging.warning(f'Retrieve object {path} error')
            raise Error(f'Retrieve object {path} error')

        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            logging.warning('Incorrect type of response data')
            raise Error('Incorrect type of response data')

    def upload_json(self, json_data: dict, file_path: str):
        s3_resource = self._get_resource()
        s3_object = s3_resource.Object(self._bucket_name, file_path)
        s3_object.put(
            Body=(bytes(json.dumps(json_data).encode('UTF-8')))
        )

    def upload_file(self, file: FileStorage, file_path: str):
        s3_resource = self._get_resource()
        s3_object = s3_resource.Object(self._bucket_name, file_path)
        s3_object.put(Body=file.read())

    def delete(self, prefix: str):
        s3_resource = self._get_resource()
        bucket = s3_resource.Bucket(self._bucket_name)
        bucket.objects.filter(Prefix=prefix).delete()

    def copy(self, key_from: str, key_to: str):
        s3_resource = self._get_resource()
        bucket = s3_resource.Bucket(self._bucket_name)
        old_source = {
            'Bucket': self._bucket_name,
            'Key': key_from,
        }
        new_obj = bucket.Object(key_to)
        new_obj.copy(old_source)

    def copy_folder(self, prefix_from: str, prefix_to: str):
        s3_resource = self._get_resource()
        bucket = s3_resource.Bucket(self._bucket_name)
        for obj in bucket.objects.filter(Prefix=prefix_from):
            new_key = obj.key.replace(prefix_from, prefix_to, 1)
            self.copy(obj.key, new_key)

    def create_invalidation(self, items: List[str]):
        client = self._get_cdn()
        client.create_invalidation(
            DistributionId=self._cdn_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(items),
                    'Items': items,
                },
                'CallerReference': str(time()).replace(".", "")
            }
        )

    def _get_resource(self):
        return boto3.resource(
            's3',
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
        )

    def _get_cdn(self) -> BaseClient:
        return boto3.client(
            'cloudfront',
            region_name=self._region,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
        )


object_storage_client = ObjectStorageAPI(
    cloud_front_base=Config.AWS_CLOUD_FRONT_DOMAIN,
    access_key=Config.AWS_ACCESS_KEY,
    secret_key=Config.AWS_SECRET_KEY,
    bucket_name=Config.S3_BUCKET_NAME,
    region=Config.AWS_REGION,
    cdn_id=Config.AWS_CLOUD_FRONT_ID,
)
