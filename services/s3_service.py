import boto3
import os
from flask import Response
from dotenv import load_dotenv


load_dotenv()


class S3bucket:
    def __init__(self):
        # S3 bucket configuration
        self.s3 = boto3.client('s3',
                               aws_access_key_id=os.environ.get('KEY'),
                               aws_secret_access_key=os.environ.get('SECRET_KEY'))
        self.bucket_name = os.environ.get('BUCKET_NAME')

    # Get all files from S3 bucket
    def get_files(self):
        files = []
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Delimiter='/')
        if response.get('Contents'):
            for obj in response['Contents']:
                obj_type = os.path.splitext(obj['Key'])[1].lstrip('.')
                files.append({'key': obj['Key'], 'size': obj['Size'], 'type': obj_type})
        if response.get('CommonPrefixes'):
            for prefix in response['CommonPrefixes']:
                files.append({'key': prefix['Prefix'].rstrip('/'), 'size': '-', 'type': 'folder'})
        return files

    # Get files in folder
    def get_files_in_folder(self, folder_path=''):
        files = []
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=f'{folder_path}/', Delimiter='/')
        if response.get('Contents'):
            for obj in response['Contents']:
                if obj['Key'] != f'{folder_path}/':
                    filename = os.path.basename(obj['Key'])
                    extension = os.path.splitext(obj['Key'])[1].lstrip('.')
                    obj_type = extension if extension else 'folder'
                    files.append({'key': filename, 'size': obj['Size'], 'type': obj_type})
        if response.get('CommonPrefixes'):
            for prefix in response['CommonPrefixes']:
                subfolder_path = prefix['Prefix'].rstrip('/')
                files.append({'key': subfolder_path, 'size': '-', 'type': 'folder'})
        return files

    # Create folder in S3 bucket
    def create_folder(self, folder_name, folder_path=''):
        if folder_path:
            key = f'{folder_path}/{folder_name}/'
        else:
            key = f'{folder_name}/'
        self.s3.put_object(Bucket=self.bucket_name, Key=key)

    # Upload file to S3 bucket
    def upload_file(self, file, folder_path=''):
        if folder_path:
            key = f'{folder_path}/{file.filename}'
        else:
            key = file.filename
        self.s3.upload_fileobj(file.stream, self.bucket_name, key)

    # Search file in S3 bucket
    def search_files(self, query, folder_path=''):
        if folder_path:
            prefix = f'{folder_path}/{query}'
        else:
            prefix = query
        files = []
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, Delimiter='/')
        for obj in response.get('Contents', []):
            filename = os.path.basename(obj['Key'])
            extension = os.path.splitext(obj['Key'])[1].lstrip('.')
            obj_type = extension if extension else 'folder'
            if obj_type != 'folder':
                files.append({'key': filename, 'size': obj['Size'], 'type': obj_type})
        for obj in response.get('CommonPrefixes', []):
            folder = obj['Prefix'].split('/')[-2]
            files.append({'key': folder, 'size': '-', 'type': 'folder'})
        return files

    # Download file from S3 bucket
    def download(self, file_name):
        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=os.environ.get('KEY'),
                                     aws_secret_access_key=os.environ.get('SECRET_KEY'))
        paginator = self.s3.get_paginator('list_objects_v2')
        key = None
        for result in paginator.paginate(Bucket=self.bucket_name):
            for item in result.get('Contents', []):
                if item['Key'].endswith(file_name):
                    key = item['Key']
        file_obj = s3_resource.Object(self.bucket_name, key).get()
        return Response(file_obj['Body'].read(),
                        mimetype='text/plain',
                        headers={"Content-Disposition": f"attachment;filename={file_name}"})
