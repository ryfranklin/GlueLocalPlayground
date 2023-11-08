import setup_database
import generate_data

from pyspark.sql import SparkSession
import threading

def read_from_sqlserver():
    # Define SQL Server connection properties
    jdbc_url = "jdbc:sqlserver://sqlserver:1433"
    connection_properties = {
        "user": "sa",
        "password": "password",
        "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    }

    # Read data from SQL Server
    df = spark.read.jdbc(url=jdbc_url,
                         table="Orders",
                         properties=connection_properties
                         )
    df.show()

def main():
    # Set up the database
    setup_database.main()

    # Start generating data in a seperate thread
    data_gen_thread = threading.Thread(target=generate_data.generate_fake_data,
                                       args=(10))  # one order per second
    data_gen_thread.start()

    # Initialzie Spark Session
    spark = SparkSession.builder.appName("AWS Glue POC with Docker").getOrCreate()

    # Define SQL Server connection properties
    read_from_sqlserver(spark)

    spark.stop()

    # Optionally wait for the data generation thread to finish
    data_gen_thread.join()
    print("Main application finished.")

if __name__ == "__main__":
    main()
