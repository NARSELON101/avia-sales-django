FROM python:3.10.12-alpine3.18
LABEL authors="danil"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["celery", "-A", "avia_ticket_sales", "beat", "-l", "info"]