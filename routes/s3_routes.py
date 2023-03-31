from flask import Blueprint, render_template, request, redirect, url_for
from services.s3_service import S3bucket
import logging
from logging.config import fileConfig
from botocore.exceptions import ClientError, EndpointConnectionError


s3_routes = Blueprint('s3_routes', __name__)
client = S3bucket()
logging.config.fileConfig(fname='logs/logging.conf')
logger = logging.getLogger('app')


@s3_routes.route('/')
def index():
    try:
        logger.info('Successful request to main page')
        return render_template('index.html')
    except Exception as e:
        logger.error(f'Connection error: {str(e)}')
        raise


@s3_routes.route('/s3_service')
def get_files():
    try:
        files = client.get_files()
        logger.info(f'Get all objects from S3 bucket {client.bucket_name}')
        return render_template('s3_service.html', files=files)
    except Exception as e:
        logger.error(f'Error in getting objects from S3 bucket {client.bucket_name}: {str(e)}')
        raise


@s3_routes.route('/s3_service/<path:folder_path>/')
def get_files_in_folder(folder_path):
    try:
        files = client.get_files_in_folder(folder_path)
        logger.info(f'Get all objects from folder {folder_path} in bucket')
        return render_template('s3_service.html', folder_name=folder_path, files=files)
    except Exception as e:
        logger.error(f'Error in getting objects from folder {folder_path}')
        raise


@s3_routes.route('/s3_service/create_folder', methods=['POST'])
def create_folder():
    try:
        foldername = request.form['foldername']
        current_path = request.form.get('current_path', '')
        client.create_folder(foldername, current_path)
        logger.info(f'Folder {foldername} was created')
        if current_path:
            return redirect(f'/s3_service/{current_path}/')
        else:
            return redirect('/s3_service')
    except Exception as e:
        logger.error(f'Error in creating folder: {str(e)}')
        raise


@s3_routes.route('/s3_service/search', methods=['POST'])
def search():
    try:
        query = request.form['query']
        current_path = request.form.get('current_path', '')
        files = client.search_files(query, current_path)
        logger.info(f"Search files with prefix {query} in S3 bucket")
        return render_template('s3_service.html', files=files)
    except Exception as e:
        logger.error(f'Error in searching files: {str(e)}')
        raise


@s3_routes.route('/s3_service/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        current_path = request.form.get('current_path', '')
        client.upload_file(file, current_path)
        logger.info(f'File {file.filename} was uploaded to S3 bucket')
        if current_path:
            return redirect(f'/s3_service/{current_path}/')
        else:
            return redirect('/s3_service')
    except ClientError as e:
        logger.error(f'Error uploading file to bucket: {str(e)}')
        raise
    except EndpointConnectionError as e:
        logger.error(f'Unable to connect to bucket endpoint: {str(e)}')
        raise


@s3_routes.route('/s3_service/download/<string:file_name>')
def download(file_name):
    try:
        file_response = client.download(file_name)
        logger.info(f'Download file {file_name} from S3 bucket')
        return file_response
    except Exception as e:
        logger.error(f'Error in downloading file {file_name} from S3 bucket: {str(e)}')
        raise
