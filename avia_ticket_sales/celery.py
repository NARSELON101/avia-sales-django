import os

from celery import Celery
from .tasks.tasks import check_notify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avia_ticket_sales.settings')

app = Celery('celery')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(100.0, check_notify.s(), name='Check users notifications')
