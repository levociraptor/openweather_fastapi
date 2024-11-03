FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y curl libpq-dev gcc \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean

ENV PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-root

COPY . /app

RUN poetry env use python \
    && poetry install --no-root

CMD ["poetry", "run", "uvicorn", "weather_api.server:app", "--host", "0.0.0.0", "--port", "8000"]