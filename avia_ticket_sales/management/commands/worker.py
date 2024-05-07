import datetime
import time
from django.core.management.base import BaseCommand
from avia_ticket_sales.utils import TIME_CHOICE
from tickets.models import TicketNotify


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            notifies = TicketNotify.objects.all()
            for notify in notifies:
                notify: TicketNotify
                last_notify = notify.last_notify
                last_notify = last_notify.strftime("%Y-%m-%d %H:%M:%S")
                last_notify = datetime.datetime.strptime(last_notify, "%Y-%m-%d %H:%M:%S")
                delay = TIME_CHOICE[notify.notify_delay]
                print(notify.ticket_uid, last_notify + delay < datetime.datetime.now())
            time.sleep(2)