import awsgi
from app import app

def lambda_handler(event, context):
    wsgi_environ = awsgi.event(event, context)
    return awsgi.response(app, wsgi_environ, context)
