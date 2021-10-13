FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

RUN apt update -y

# Need gcc for building RPi.GPIO
RUN apt install gcc -y

RUN adduser --disabled-password --gecos '' api
USER api

COPY --chown=api:api requirements.txt .

# RUN apk add --update alpine-sdk

# Fix for pip install RPi.GPIO
ENV CFLAGS "-fcommon"

RUN pip install -r requirements.txt --no-cache-dir --user

ENV PATH="/home/api/.local/bin:${PATH}"

COPY --chown=api:api app/ /app

