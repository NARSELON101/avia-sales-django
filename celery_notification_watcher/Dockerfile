FROM python:3.10.12-alpine3.18
LABEL authors="danil"

WORKDIR /app
RUN mkdir "celery_notification_watcher"
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app/celery_notification_watcher


CMD ["celery", "-A", "celery_notification_watcher", "worker", "-l", "info"]