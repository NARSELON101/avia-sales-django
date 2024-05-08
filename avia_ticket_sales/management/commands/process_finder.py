import time

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from avia_ticket_sales import settings
import psutil
from avia_ticket_sales.utils import connect

import json


class Command(BaseCommand):
    """ Listener RabbitMQ очереди """
    def handle(self, *args, **options):
        pool = set()
        while True:
            for process in psutil.process_iter(['cmdline']):
                try:
                    if self.is_django_background_command(process):
                        if process not in pool:
                            pool.add(process)
                            print()
                            print(f"Найдена фоновая команда Django с PID {process.pid} - {process.name}")
                            print()
                except Exception:
                    pass
            print([proc.status() for proc in pool])
            time.sleep(15)
    @staticmethod
    def is_django_background_command(process):
        try:
            cmdline = process.cmdline()
            if 'manage.py' in cmdline and 'runserver' not in cmdline:
                return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
        return False

