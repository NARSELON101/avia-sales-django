import os
from datetime import datetime, timedelta

from celery import Celery

from celery_notification_watcher.database import SessionLocal
from celery_notification_watcher.models import TicketNotify, Ticket
from celery_notification_watcher.repository import TicketNotificationRepository, \
    NewsRepository, UsersRepository, TicketsRepository
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
messages_repo = NewsRepository(SessionLocal)
users_repo = UsersRepository(SessionLocal)
tickets_repo = TicketsRepository(SessionLocal)


@app.task
def check_newsletter():
    messages_list = messages_repo.all()
    if messages_list:
        row = messages_list[0]
        email_subjects = [row.email for row in users_repo.get_notified_users()]
        email_sander.delay(email_subjects, row.message)
        messages_repo.delete(row)


@app.task
def check_ticket_confirm():
    if not eval(os.environ.get("AUTO_CONFIRM", True)):
        for ticket in tickets_repo.all():
            ticket: Ticket
            if ticket.reserve_time \
                    and not ticket.is_confirmed \
                    and format_time(ticket.reserve_time) + timedelta(minutes=15) < datetime.now():
                print(f"Бронь на билет с ID {ticket.ticket_uid} Отменена")
                ticket.auth_user = None
                ticket.reserve_time = None
                ticket.is_confirmed = True
                tickets_repo.save(ticket)


@app.task
def check_notify():
    notifies = notification_repo.all()
    for notify in notifies:
        notify: TicketNotify

        last_notify = format_time(notify.last_notify)

        delay = TIME_CHOICE[notify.notify_delay]
        current_time = datetime.now()

        if last_notify + delay < current_time:
            message = create_message(notify.tickets_ticket,
                                     notify.auth_user)
            # Вызвать отправку письма
            email_sander.delay([notify.auth_user.email], message)

            notify.last_notify = current_time
            notification_repo.save(notify)


def format_time(time_str):
    time_str = time_str.strftime("%Y-%m-%d %H:%M:%S")
    time_str = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return time_str


def create_message(ticket, user):
    """ Создание сообщения для последующей отправки в RabbitMQ"""
    message = f'Добрый день {user.first_name}! Напоминаем вам о билете ' \
              f'в {ticket.to_country} из {ticket.from_country}. ' \
              f'Дата рейса: {ticket.flight_date}. Обратный рейс: {ticket.back_date}'
    return message
