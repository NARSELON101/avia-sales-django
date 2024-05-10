import smtplib

from celery import Celery

from .config import *

app = Celery("email_sander",
             broker=CELERY_BROKER_URL or f"amqp://{RMQ_USER}:{RMQ_PASS}@{RMQ_HOST}:{RMQ_PORT}/",
             timezone=TIME_ZONE)

__all__ = (app,)


@app.task
def email_sander(emails: list[str], message: str):
    if WRITE_TO_CONSOLE:
        print(emails)
        print(message)
        return
    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            print(f"Получено сообщение")
            email_subject = "Напоминание о бронировании билета"
            for email in emails:
                server.sendmail(EMAIL_HOST_USER, email, f"Subject: {email_subject}\n\n{message}")
    except Exception as error:
        print("ERR", error)
