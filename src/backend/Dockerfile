FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
