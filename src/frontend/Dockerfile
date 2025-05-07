FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD ["streamlit", "run", "home.py", "--server.port=8501"]
