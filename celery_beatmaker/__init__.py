from celery import Celery

from .config import *

app = Celery("beat_maker",
             broker=CELERY_BROKER_URL or f"amqp://{RMQ_USER}:{RMQ_PASS}@{RMQ_HOST}:{RMQ_PORT}/",
             timezone=TIME_ZONE)

# __all__ = (app,)

check_notify = app.signature("celery_notification_watcher.check_notify")
check_newsletter = app.signature("celery_notification_watcher.check_newsletter")
check_confirmed = app.signature("celery_notification_watcher.check_ticket_confirm")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(NOTIFICATION_CHECK_TIME, check_notify, name='Check users notifications')
    sender.add_periodic_task(NOTIFICATION_CHECK_TIME, check_newsletter, name='Check newsletters')
    sender.add_periodic_task(NOTIFICATION_CHECK_TIME, check_confirmed, name='Check tickets confirm')
