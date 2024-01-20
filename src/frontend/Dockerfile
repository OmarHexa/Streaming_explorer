FROM python:3.9

COPY ./frontend /app

WORKDIR /app

RUN pip install -r requirements.txt  # Adjust based on your actual requirements

CMD ["streamlit", "run", "home.py", "--server.port", "8501"]
