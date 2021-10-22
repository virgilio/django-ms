# syntax=docker/dockerfile:1
FROM python:3-alpine
ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /requirements.txt

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN python -m pip install -r /requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

COPY app /app/
