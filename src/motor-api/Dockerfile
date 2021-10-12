FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

RUN apt update -y
RUN apt install gcc -y

RUN adduser --disabled-password --gecos '' api
USER api

COPY --chown=api:api requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir --user

ENV PATH="/home/api/.local/bin:${PATH}"

COPY --chown=api:api src/ /app