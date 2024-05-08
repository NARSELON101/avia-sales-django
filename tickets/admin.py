import multiprocessing
import os
import signal
import subprocess
import threading
import typing

import django
from django.contrib import admin
from concurrent.futures import ProcessPoolExecutor
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from tickets.models import Ticket, TicketNotify
from django.core.management import call_command
from django.db import models
# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(TicketNotify)
class TicketNotifyAdmin(admin.ModelAdmin):
    pass


class BackgroundTasksTypes(models.TextChoices):
    WORKER = 'worker', _("Фоновый обработчик напоминаний")
    LISTENER = 'listener', _("Фоновый обработчик очереди RabbitMQ")


class BackgroundTask(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    background_type = models.TextField(choices=BackgroundTasksTypes.choices)

    def __str__(self):
        return self.name


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class MyModelAdmin(admin.ModelAdmin):
    list_display = ['background_type', 'name', 'description', 'run_command_button']

    commands_pool: typing.Dict[str, typing.Any] = {}

    def run_command_button(self, obj: BackgroundTask):
        if obj.background_type not in self.commands_pool:
            return format_html('<a class="button" href="{}">Run Command</a>',
                               reverse('admin:run_command_view', args=[obj.background_type]))
        else:
            return format_html('<a class="button" href="{}" style="active: false">Stop Command</a>',
                               reverse('admin:stop_command_execute', args=[obj.background_type]))

    run_command_button.short_description = 'Run Command'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('run_command/<str:background_type>/', self.run_command_view, name='run_command_view'),
            path('stop_command/<str:background_type>/', self.stop_command_execute, name='stop_command_execute'),
        ]
        return custom_urls + urls

    @staticmethod
    def subprocess_setup():
        django.setup()

    def run_command_view(self, request, background_type):
        try:
            if background_type not in self.commands_pool:
                process = StoppableThread(target=call_command, args={background_type})
                self.commands_pool[background_type] = process
                process.start()
                print("START THREAD - ", background_type)
            else:
                print(f"COMMAND {background_type} STARTED ALREADY")

        except Exception as e:
            pass
        return redirect("admin/")

    def stop_command_execute(self, request, background_type):
        try:
            process = self.commands_pool.pop(background_type)
            process.stop()
        except Exception as e:
            print("ERR - ", e)

        return redirect('admin/')


admin.site.register(BackgroundTask, MyModelAdmin)
