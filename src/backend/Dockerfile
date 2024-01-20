FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./backend /app

WORKDIR /app

RUN pip install -r requirements.txt  # Adjust based on your actual requirements

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
