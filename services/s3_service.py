import boto3
import os
import logging
from logging.config import fileConfig
from flask import Response
from dotenv import load_dotenv
from botocore.exceptions import ClientError, EndpointConnectionError


load_dotenv()
logging.config.fileConfig(fname='logs/logging.conf')
logger = logging.getLogger('s3service')


class S3bucket:
    def __init__(self):
        # S3 bucket configuration
        self.s3 = boto3.client('s3',
                               aws_access_key_id=os.environ.get('KEY'),
                               aws_secret_access_key=os.environ.get('SECRET_KEY'))
        self.bucket_name = os.environ.get('BUCKET_NAME')

    # Get all files from S3 bucket
    def get_files(self):
        try:
            files = []
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if response.get('Contents'):
                for obj in response['Contents']:
                    files.append({'key': obj['Key'], 'size': obj['Size']})
            logger.info(f'Get all files from S3 bucket {self.bucket_name}')
            return files
        except Exception as e:
            logger.error(f'Error in getting files from S3 bucket {self.bucket_name}: {str(e)}')
            raise

    # Upload file to S3 bucket
    def upload_file(self, file):
        try:
            self.s3.upload_fileobj(file.stream, self.bucket_name, file.filename)
            logger.info(f'File {file.filename} was uploaded to S3 bucket')
        except ClientError as e:
            logger.error(f'Error uploading file to bucket: {str(e)}')
            raise
        except EndpointConnectionError as e:
            logger.error(f'Unable to connect to bucket endpoint: {str(e)}')
            raise

    # Search file in S3 bucket
    def search_files(self, query):
        try:
            files = []
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=query)
            if response.get('Contents'):
                for obj in response['Contents']:
                    files.append({'key': obj['Key'], 'size': obj['Size']})
            logger.info(f"Search files with prefix '{query}' in bucket: {files}")
            return files
        except Exception as e:
            logger.error(f"Error in searching files: {str(e)}")
            raise

    # Download file from S3 bucket
    def download(self, filename):
        try:
            s3_resource = boto3.resource('s3',
                                         aws_access_key_id=os.environ.get('KEY'),
                                         aws_secret_access_key=os.environ.get('SECRET_KEY'))
            file_obj = s3_resource.Object(os.environ.get('BUCKET_NAME'), filename).get()
            logger.info(f"Download file {filename} from bucket")
            return Response(
                file_obj['Body'].read(),
                mimetype='text/plain',
                headers={"Content-Disposition": f"attachment;filename={filename}"}
            )
        except Exception as e:
            logger.error(f'Error in downloading file {filename} from bucket: {str(e)}')
            raise
