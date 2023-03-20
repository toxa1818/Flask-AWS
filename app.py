from flask import Flask, render_template, request, redirect, url_for
from services.s3_service import S3bucket
import logging
from logging.config import fileConfig


app = Flask(__name__)
client = S3bucket()
logging.config.fileConfig(fname='logs/logging.conf')
logger = logging.getLogger('app')


@app.route('/')
def index():
    try:
        logger.info('Successful request to main page')
        files = client.get_files()
        return render_template('index.html', files=files)
    except Exception as e:
        logger.error(f'Connection error: {str(e)}')
        raise


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    files = client.search_files(query)
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    client.upload_file(file)
    return redirect(url_for('index'))


@app.route('/download/<string:filename>')
def download(filename):
    file_response = client.download(filename)
    return file_response


if __name__ == '__main__':
    app.run(debug=True)
