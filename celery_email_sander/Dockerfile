FROM python:3.10.12-alpine3.18
LABEL authors="danil"

WORKDIR /app
RUN mkdir "celery_email_sander"
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app/celery_email_sander

CMD ["celery", "-A", "celery_email_sander", "worker", "-l", "info", "-Q", "email_sander"]