FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

LABEL MAINTAINER="Avyay jain <avyay.jain2001@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . /app

WORKDIR /app

COPY . .

ADD requirements.txt .

RUN pip install -r requirements.txt

CMD fastapi dev main.app