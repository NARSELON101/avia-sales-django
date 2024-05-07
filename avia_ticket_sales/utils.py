import datetime

import pika
import time

from avia_ticket_sales import settings

TIME_CHOICE = {"one_hour": datetime.timedelta(hours=1),
               'three_hours': datetime.timedelta(hours=3),
               'one_day': datetime.timedelta(days=1),
               'one_week': datetime.timedelta(weeks=1)
               }


def connect(queue='notifies', retry=True):
    connected = False
    while not connected:
        try:
            credentials = pika.PlainCredentials(username=settings.RMQ_USER,
                                                password=settings.RMQ_PASS)
            parameters = pika.ConnectionParameters(host=settings.RMQ_HOST,
                                                   port=settings.RMQ_PORT, credentials=credentials)
            connection = pika.BlockingConnection(parameters=parameters)
            channel = connection.channel()
            channel.queue_declare(queue=queue)
            connected = True
            return connection, channel
        except Exception:
            pass
        if not retry:
            return None, None
        time.sleep(5)
