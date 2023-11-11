# Use a Python base image
FROM python:3.8-slim-bullseye

# Install system dependencies required for PyODBC and other Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        g++ \
        unixodbc-dev \
        gnupg \
        gnupg2 \
        gnupg1 \
        curl \
    && apt-get install -y openjdk-11-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install the Microsoft ODBC Driver for SQL Server
RUN curl -s https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/10/prod buster main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download the SQL Server JDBC driver
COPY mssql-jdbc-12.4.2.jre8.jar /opt/mssql-jdbc.jar


# Set Java environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $PATH:$JAVA_HOME/bin

# Install AWS CLI
RUN pip install awscli

# Install PySpark and Boto3 for AWS interactions
RUN pip install pyspark boto3 pyodbc

# Copy your ETL script into the container
COPY main.py /main.py
COPY generate_data.py /generate_data.py
COPY setup_database.py /setup_database.py
COPY ddl.sql /ddl.sql

# Install any dependencies


# Command to run the main script when the container starts
CMD ["python", "/main.py"]