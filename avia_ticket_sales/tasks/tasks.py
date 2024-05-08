import json
from datetime import datetime, timedelta

from celery import shared_task

TIME_CHOICE = {"one_hour": timedelta(hours=1),
               'three_hours': timedelta(hours=3),
               'one_day': timedelta(days=1),
               'one_week': timedelta(weeks=1)
               }


@shared_task
def check_notify():
    from tickets.models import TicketNotify

    notifies = TicketNotify.objects.all()
    for notify in notifies:
        print(notify)
        notify: TicketNotify

        last_notify = notify.last_notify
        last_notify = last_notify.strftime("%Y-%m-%d %H:%M:%S")
        last_notify = datetime.strptime(last_notify, "%Y-%m-%d %H:%M:%S")
        delay = TIME_CHOICE[notify.notify_delay]
        current_time = datetime.now()

        if last_notify + delay < current_time:
            message = create_message(notify.ticket_uid,
                                     notify.user_uid)
            # Вызвать отправку письма
            email_sander.delay([notify.user_uid.email], message)

            notify.last_notify = current_time
            notify.save()
            print(last_notify, ">", notify.ticket_uid.ticket_uid, notify.ticket_uid.price)


def create_message(ticket, user):

    """ Создание сообщения для последующей отправки в RabbitMQ"""
    message = f'Добрый день {user.first_name}! Напоминаем вам о билете ' \
              f'в {ticket.to_country} из {ticket.from_country}. ' \
              f'Дата рейса: {ticket.flight_date}. Обратный рейс: {ticket.back_date}'
    return message


@shared_task
def email_sander(emails: list[str], message: str):
    from django.conf import settings
    from django.core.mail import send_mail
    try:
        print(f"Получено сообщение")
        email_subject = "Напоминание о бронировании билета"
        send_mail(email_subject, message, settings.EMAIL_HOST_USER, emails, fail_silently=True)
    except Exception as error:
        print("ERR", error)
