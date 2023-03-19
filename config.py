import os
from dotenv import load_dotenv


load_dotenv()
S3_BUCKET_CREDS = {'key': os.getenv('KEY'),
                   'secret_key': os.getenv('SECRET_KEY'),
                   'bucket_name': os.getenv('BUCKET_NAME')}
