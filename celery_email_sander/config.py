from os import environ

RMQ_USER = environ.get('RMQ_USER', 'guest')
RMQ_PASS = environ.get('RMQ_PASS', 'guest')
RMQ_HOST = environ.get('RMQ_HOST', '127.0.0.1')
RMQ_PORT = environ.get('RMQ_PORT', 5672)

TIME_ZONE = environ.get('TIME_ZONE', 'UTC')

CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL", None)

WRITE_TO_CONSOLE = environ.get("WRITE_TO_CONSOLE", "True")

EMAIL_HOST = environ.get("EMAIL_HOST")
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = environ.get("EMAIL_PORT")
