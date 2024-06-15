FROM python:3.9-slim

# set work directory
WORKDIR /api

# set .env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .