from decouple import config


S3_BUCKET_CREDS = {'key': config('KEY', default=''),
                   'secret_key': config('SECRET_KEY', default=''),
                   'bucket_name': config('BUCKET_NAME', default='')}
