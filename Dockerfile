# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN pip install "poetry==1.1.12"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /app

ENTRYPOINT ["python", "./main.py"]
CMD []
