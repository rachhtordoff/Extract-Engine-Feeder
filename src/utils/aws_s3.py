# aws_service.py
import boto3
from botocore.client import Config
from src import config
import os

class AWSService:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            config=Config(signature_version='s3v4'),
            region_name='eu-west-2'
        )

    def download_file(self, folder_id, doc_name):
        bucket_name = f'{config.BUCKET_ID}'
        newdoc_name = f'{config.BUCKET_NAME}/uploads/{folder_id}/{doc_name}'
        copy_doc_name = f'/opt/src/documents/{doc_name}'
        
        self.client.download_file(bucket_name, newdoc_name, copy_doc_name)

    def get_folder_list(self, folder_id, doc_name):
        folder_list = []
        local_directory = f'/opt/src/documents/{doc_name}'

        # Prefix to search in the bucket.
        prefix = f'{config.BUCKET_NAME}/uploads/{folder_id}/{doc_name}'

        # List objects within the bucket with the specified prefix.
        response = self.client.list_objects_v2(Bucket=config.BUCKET_ID, Prefix=prefix)

        # Check if any contents are found.
        if 'Contents' in response:
            for obj in response['Contents']:
                key_suffix = obj['Key'][len(prefix):].lstrip('/')
                if not os.path.basename(key_suffix).startswith('.'):
                    trimmed_key = os.path.join(doc_name, key_suffix)
                    folder_list.append(trimmed_key)

        return folder_list
