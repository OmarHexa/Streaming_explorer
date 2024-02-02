FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src /app/src
COPY requirements.txt /app
COPY pyproject.toml /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000


# Command to run the application
CMD ["uvicorn", "src.backend.app:app", "--host", "127.0.0.1", "--port", "8000"]


# Use the official Python image with the specified version
# FROM python:3.11

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY src /app/src
# COPY requirements.txt /app
# COPY pyproject.toml /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Use wget to download the MySQL Connector
# RUN apt-get update && apt-get install -y wget \
#     && wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.23.tar.gz\
#     && tar -xzf mysql-connector-java-8.0.23.tar.gz \
#     && mv mysql-connector-java-8.0.23/mysql-connector-java-8.0.23.jar /usr/local/lib/python3.11/site-packages/pyspark/jars \
#     && rm -rf mysql-connector-java-8.0.23*

# # Set environment variables for Java and MySQL Connector
# ENV JAVA_HOME=/usr/local/openjdk-11
# ENV PATH=$PATH:/usr/local/openjdk-11/bin
# ENV CLASSPATH=/app/mysql-connector-java-8.3.0.jar

# # Expose the port the app runs on
# EXPOSE 8000

# # Command to run the application
# CMD ["uvicorn", "src.backend.app:app", "--host", "127.0.0.1", "--port", "8000"]
