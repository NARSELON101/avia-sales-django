from datetime import datetime, timedelta

from celery import Celery

from celery_notification_watcher.database import SessionLocal
from celery_notification_watcher.models import TicketNotify
from celery_notification_watcher.repository import TicketNotificationRepository
from .config import *

app = Celery("notification_watcher",
             broker=f"amqp://{RMQ_USER}:{RMQ_PASS}@{RMQ_HOST}:{RMQ_PORT}/",
             timezone=TIME_ZONE)

__all__ = (app,)

app.conf.task_routes = TASK_ROUTE

email_sander = app.signature("celery_email_sander.email_sander")

TIME_CHOICE = {"one_hour": timedelta(hours=1),
               'three_hours': timedelta(hours=3),
               'one_day': timedelta(days=1),
               'one_week': timedelta(weeks=1)
               }

notification_repo = TicketNotificationRepository(SessionLocal)


@app.task
def check_notify():
    notifies = notification_repo.all()
    for notify in notifies:
        notify: TicketNotify

        last_notify = notify.last_notify
        last_notify = last_notify.strftime("%Y-%m-%d %H:%M:%S")
        last_notify = datetime.strptime(last_notify, "%Y-%m-%d %H:%M:%S")
        delay = TIME_CHOICE[notify.notify_delay]
        current_time = datetime.now()

        if last_notify + delay < current_time:
            message = create_message(notify.tickets_ticket,
                                     notify.auth_user)
            # Вызвать отправку письма
            email_sander.delay([notify.auth_user.email], message)

            notify.last_notify = current_time
            notification_repo.save(notify)


def create_message(ticket, user):
    """ Создание сообщения для последующей отправки в RabbitMQ"""
    message = f'Добрый день {user.first_name}! Напоминаем вам о билете ' \
              f'в {ticket.to_country} из {ticket.from_country}. ' \
              f'Дата рейса: {ticket.flight_date}. Обратный рейс: {ticket.back_date}'
    return message
