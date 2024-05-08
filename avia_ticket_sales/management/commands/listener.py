from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from pika.exceptions import StreamLostError

from avia_ticket_sales import settings

from avia_ticket_sales.utils import connect

import json


class Command(BaseCommand):
    """ Listener RabbitMQ очереди """
    def handle(self, *args, **options):
        connection, channel = connect()
        print("Слушатель очереди в Rabbit. Для выхода нажмите CTRL+C")
        channel.basic_consume(queue='notifies', auto_ack=True,
                              on_message_callback=self.callback)
        try:
            channel.start_consuming()
        except StreamLostError:
            self.handle(*args, **options)

    @staticmethod
    def callback(ch, method, properties, body):
        """ Получаем сообщения в json формате, где передаем Email, Message.
         Message - заранее сформированная строка, где указана информация о билете
         Email - email, под которым зарегистрирован пользователь
         """
        try:
            print(f"Получено сообщение")
            response = json.loads(body.decode("utf-8")).get("response")
            to_list = response.get('email')
            message = response.get('message')
            email_subject = "Напоминание о бронировании билета"
            send_mail(email_subject, message, settings.EMAIL_HOST_USER, [to_list], fail_silently=True)
        except Exception as error:
            print("ERR", error)
