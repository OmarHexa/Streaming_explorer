FROM python:3.11-slim
# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . .
# install all the requirements
RUN pip install poetry && poetry install
CMD ["streamlit", "run", "home.py", "--server.port", "8501"]
