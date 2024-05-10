from os import environ

ECHO = False
DATABASE_URL = "sqlite:///db/db.sqlite3"

RMQ_USER = environ.get('RMQ_USER', 'guest')
RMQ_PASS = environ.get('RMQ_PASS', 'guest')
RMQ_HOST = environ.get('RMQ_HOST', '127.0.0.1')
RMQ_PORT = environ.get('RMQ_PORT', 5672)

TIME_ZONE = environ.get('TIME_ZONE', 'UTC')

TASK_ROUTE = {
    "celery_email_sander.email_sander": {"queue": "email_sander"}
}
