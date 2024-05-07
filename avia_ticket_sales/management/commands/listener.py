from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image

from avia_ticket_sales.utils import connect

import io
import os
from io import BytesIO
import urllib.parse
import base64
import pika
import time
import json


class Command(BaseCommand):
    """ Listener RabbitMQ очереди """
    def handle(self, *args, **options):
        connection, channel = connect()
        print("Слушатель очереди в Rabbit. Для выхода нажмите CTRL+C")
        channel.basic_consume(queue='notifies', auto_ack=True,
                              on_message_callback=self.callback)
        channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        """ Получаем сообщения в json формате, где передаем Email, Message.
         Message - заранее сформированная строка, где указана информация о билете
         Email - email, под которым зарегистрирован пользователь
         """
        try:
            print(f"Processing")
            res = json.loads(body.decode("utf-8"))
            print(res)
            print("Processing image 'to_resize' complete")
        except Exception as error:
            print(error)
