import os
# For logging
FLASK_LOG_LEVEL = os.environ['FLASK_LOG_LEVEL']
APP_NAME = os.environ['APP_NAME']
SQS_QUEUE_NAME = os.environ['SQS_QUEUE_NAME']
user_api_url = os.environ['user_api_url']
openapi_api_url = os.environ['openapi_api_url']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
email_api_url = os.environ['email_api_url']
POLLING_INTERVAL = int(os.environ['POLLING_INTERVAL'])
SECRET_KEY = os.environ["SECRET_KEY"]


aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key']

try:
    LOCALSQS = os.environ['LOCALSQS']
except:
    LOCALSQS = "false"
