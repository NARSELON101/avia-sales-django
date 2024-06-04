from os import environ

RMQ_USER = environ.get('RMQ_USER', 'guest')
RMQ_PASS = environ.get('RMQ_PASS', 'guest')
RMQ_HOST = environ.get('RMQ_HOST', '127.0.0.1')
RMQ_PORT = environ.get('RMQ_PORT', 5672)

CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL", None)

TIME_ZONE = environ.get('TIME_ZONE', 'UTC')

NOTIFICATION_CHECK_TIME = int(environ.get('NOTIFICATION_CHECK_TIME', 10))
