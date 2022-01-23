FROM python:3.10-alpine as base


ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update -y && \
    apt-get clean


RUN pip install poetry

WORKDIR /script
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev


COPY ./entrypoint.sh /entrypoint.sh


COPY ./ .

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
