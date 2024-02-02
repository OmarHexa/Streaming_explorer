FROM python:3.11

# Copy the current directory contents into the container at /app
COPY src /app/src
COPY requirements.txt /app
COPY pyproject.toml /app


# Set the working directory in the container
WORKDIR /app
# install all the requirements
RUN pip install -r requirements.txt

CMD ["streamlit", "run", "src/frontend/home.py", "--server.port", "8501"]
