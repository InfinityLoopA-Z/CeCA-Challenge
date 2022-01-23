FROM python:3.10 as base


ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=false


RUN pip install poetry

WORKDIR /script
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev


COPY ./entrypoint.sh /entrypoint.sh


COPY ./ .

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "load_db.py"]
