FROM python:3.13-slim

WORKDIR /code
ENV PYTHONPATH=/code
COPY pyproject.toml poetry.lock* /code/

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install poetry
RUN pip install fastapi
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
RUN pip install psycopg2
COPY . /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
