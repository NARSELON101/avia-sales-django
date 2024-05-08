FROM python:3.10.12-alpine3.18
LABEL authors="danil"

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["celery", "-A", "avia_ticket_sales", "worker", "-l", "info"]