FROM python:3.11-slim
# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . .
# Install any needed packages specified in requirements.txt
RUN pip install poetry && poetry install
# Command to run the application
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]