import os

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html

from env_configuration.models import EnvironmentNames


@admin.register(EnvironmentNames)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'run_command_button']

    def run_command_button(self, obj):
        print(os.environ)
        if eval(os.environ.get("AUTO_CONFIRM", "True")):
            return format_html('<a class="button" href="{}">Отключить автоподтверждение</a>',
                               reverse('admin:disable_auto_confirm', args=[obj.id]))
        else:
            return format_html('<a class="button" href="{}">Включить автоподтверждение</a>',
                               reverse('admin:enable_auto_confirm', args=[obj.id]))

    run_command_button.short_description = 'Run Command'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('disable_auto_confirm/<int:object_id>/', self.disable_auto_confirm, name='disable_auto_confirm'),
            path('enable_auto_confirm/<int:object_id>/', self.enable_auto_confirm, name='enable_auto_confirm'),
        ]
        return custom_urls + urls

    def disable_auto_confirm(self, request, object_id):
        try:
            os.environ['AUTO_CONFIRM'] = "False"
            print("Отключение авто подтверждения")
        except Exception as e:
            print("Ошибка False")

        return redirect("/admin/env_configuration/environmentnames")

    def enable_auto_confirm(self, request, object_id):
        try:
            # Здесь вы можете вызвать нужную вам команду Django
            os.environ['AUTO_CONFIRM'] = "True"
            print("Включение авто подтверждения")
        except Exception as e:
            print("Ошибка True")

        return redirect("/admin/env_configuration/environmentnames/")
