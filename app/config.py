from dotenv import load_dotenv
from os import environ
load_dotenv()

AWS_S3_BUCKET = environ.get('AWS_S3_BUCKET')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = environ.get('AWS_REGION_NAME')