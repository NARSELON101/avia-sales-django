import datetime
import json
import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from avia_ticket_sales.utils import connect
from tickets.models import TicketNotify, Ticket

TIME_CHOICE = {"one_hour": datetime.timedelta(hours=1),
               'three_hours': datetime.timedelta(hours=3),
               'one_day': datetime.timedelta(days=1),
               'one_week': datetime.timedelta(weeks=1)
               }


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Запуск фонового обработчика напоминаний о бронировании билета
        Берет все записи из таблицы с напоминаниями, и если время последнего напоминания + частота напоминания
        меньше текущего времени, то отправляет сообщение в очередь RabbitMQ,
         и перезаписывает время последнего напоминания
        """
        connection, channel = connect()

        while True:
            print("working")
            notifies = TicketNotify.objects.all()
            for notify in notifies:
                notify: TicketNotify

                last_notify = notify.last_notify
                last_notify = last_notify.strftime("%Y-%m-%d %H:%M:%S")
                last_notify = datetime.datetime.strptime(last_notify, "%Y-%m-%d %H:%M:%S")
                delay = TIME_CHOICE[notify.notify_delay]
                current_time = datetime.datetime.now()

                if last_notify + delay < current_time:
                    message = self.create_message(notify.ticket_uid,
                                                  notify.user_uid)
                    body = json.dumps({'response': {'email': notify.user_uid.email, "message": message}})
                    channel.basic_publish(exchange='', routing_key='notifies', body=body)

                    notify.last_notify = current_time
                    notify.save()
                    print(last_notify, ">", notify.ticket_uid.ticket_uid, notify.ticket_uid.price)
            time.sleep(2)

    @staticmethod
    def create_message(ticket: Ticket, user: User):
        """ Создание сообщения для последующей отправки в RabbitMQ"""
        message = f'Добрый день {user.first_name}! Напоминаем вам о билете ' \
                  f'в {ticket.to_country} из {ticket.from_country}. ' \
                  f'Дата рейса: {ticket.flight_date}. Обратный рейс: {ticket.back_date}'

        return message
