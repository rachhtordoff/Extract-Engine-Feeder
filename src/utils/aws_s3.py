# aws_service.py
import boto3
from botocore.client import Config
from src import config

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
