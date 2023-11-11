import setup_database
import generate_data
from time import sleep
from pyspark.sql import SparkSession
import threading

def read_from_sqlserver(spark):
    # Define SQL Server connection properties
    jdbc_url = "jdbc:sqlserver://sqlserver:1433;"\
        "encrypt=true;trustServerCertificate=true;"\
        "database=TestDB;"
    connection_properties = {
        "user": "sa",
        "password": "Password!123",
        "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    }

    # Read data from SQL Server
    df = spark.read.jdbc(url=jdbc_url,
                         table="Orders",
                         properties=connection_properties
                         )
    return df

def main():
    # Set up the database
    setup_database.main()

    # Start generating data in a seperate thread
    data_gen_thread = threading.Thread(target=generate_data.generate_fake_data,
                                       args=(1,))  # one order per second
    data_gen_thread.start()

    # Initialzie Spark Session
    spark = SparkSession.builder.appName("AWS Glue POC with Docker")\
        .config("spark.jars", "/opt/mssql-jdbc.jar")\
        .getOrCreate()

    # Define SQL Server connection properties
    while True:
        df = read_from_sqlserver(spark)
        df.show()
        sleep(10)

    spark.stop()

    # Optionally wait for the data generation thread to finish
    data_gen_thread.join()
    print("Main application finished.")

if __name__ == "__main__":
    main()
