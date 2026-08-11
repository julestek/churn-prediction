FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry --no-cache-dir

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main --no-root

COPY src/ ./src/

ARG KAGGLE_API_TOKEN
RUN mkdir -p ~/.kaggle \
    && echo "$KAGGLE_API_TOKEN" > ~/.kaggle/access_token \
    && chmod 600 ~/.kaggle/access_token \
    && poetry run kaggle datasets download -d blastchar/telco-customer-churn -p data/ --unzip \
    && poetry run python -m src.train

EXPOSE 8000

CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}