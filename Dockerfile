# Use a Python base image
FROM python:3.8-slim-bullseye

# Install Java (required for Spark)
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

# Set Java environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $PATH:$JAVA_HOME/bin

# Install AWS CLI
RUN pip install awscli

# Install PySpark and Boto3 for AWS interactions
RUN pip install pyspark boto3

# Copy your ETL script into the container
COPY main.py /main.py
COPY generate_data.py /generate_data.py
COPY setup_database.py /setup_database.py
COPY ddl.sql /ddl.sql

