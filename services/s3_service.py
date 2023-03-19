import boto3
from flask import Response
from config import S3_BUCKET_CREDS


class S3bucket:
    def __init__(self):
        # S3 bucket configuration
        self.s3 = boto3.client('s3',
                               aws_access_key_id=S3_BUCKET_CREDS['key'],
                               aws_secret_access_key=S3_BUCKET_CREDS['secret_key'])
        self.bucket_name = S3_BUCKET_CREDS['bucket_name']

    # Get all files from S3 bucket
    def get_files(self):
        files = []
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        if response.get('Contents'):
            for obj in response['Contents']:
                files.append({'key': obj['Key'], 'size': obj['Size']})
        return files

    # Upload file to S3 bucket
    def upload_file(self, file):
        self.s3.upload_fileobj(file.stream, self.bucket_name, file.filename)

    # Search file in S3 bucket
    def search_files(self, query):
        files = []
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=query)
        if response.get('Contents'):
            for obj in response['Contents']:
                files.append({'key': obj['Key'], 'size': obj['Size']})
        return files

    # Download file from S3 bucket
    def download(self, filename):
        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=S3_BUCKET_CREDS['key'],
                                     aws_secret_access_key=S3_BUCKET_CREDS['secret_key'])
        file_obj = s3_resource.Object(S3_BUCKET_CREDS['bucket_name'], filename).get()
        return Response(
            file_obj['Body'].read(),
            mimetype='text/plain',
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
