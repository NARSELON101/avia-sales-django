FROM python:3.10.12-alpine3.18
LABEL authors="danil"

WORKDIR /app
RUN mkdir "celery_beatmaker"
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app/celery_beatmaker

CMD ["celery", "-A", "celery_beatmaker", "beat", "-l", "info"]