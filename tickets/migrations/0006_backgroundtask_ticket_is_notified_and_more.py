# Generated by Django 5.0.4 on 2024-05-08 09:53

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_ticket_user_model'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('background_type', models.TextField(choices=[('worker', 'Фоновый обработчик напоминаний'), ('listener', 'Фоновый обработчик очереди RabbitMQ')])),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_notified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='user_model',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='TicketNotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_delay', models.TextField(choices=[('one_hour', 'Каждый час'), ('three_hours', 'Каждые 3 часа'), ('one_day', 'Каждый день'), ('one_week', 'Каждая неделя')])),
                ('last_notify', models.DateTimeField(default=datetime.datetime.now)),
                ('ticket_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_id', to='tickets.ticket')),
                ('user_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
