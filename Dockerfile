FROM python:3.10.12-alpine3.18
LABEL authors="danil"

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["sh", "start.sh"]