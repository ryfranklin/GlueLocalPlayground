import pyodbc
import time



def run_ddl_script(cursor, ddl_script):
    with open(ddl_script, 'r') as file:
        # Assume each statement is separated by a semicolon and a newline
        ddl_statements = file.read().split(';\n')
        for statement in ddl_statements:
            # Skip any empty statements resulting from the split
            if statement.strip() == '':
                continue
            cursor.execute(statement)
            cursor.commit()  # Commit after each statement

def create_connection():
    retries = 5
    conn = None
    while retries > 0:
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=sqlserver;'
                'DATABASE=master;'
                'UID=sa;'
                'PWD=Password!123',
                autocommit=True,
                timeout=5)
            
            if conn:
                break

        except pyodbc.OperationalError:
            print("Waiting for SQL Server to start...")
            time.sleep(5)
            retries -= 1
    return conn

def main():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Disconnect all connections to the database
            cursor.execute("DROP DATABASE IF EXISTS TestDB")
            cursor.execute("CREATE DATABASE TestDB")
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            cursor.rollback()
        cursor.execute("USE TestDB")
        run_ddl_script(cursor, 'ddl.sql')
        cursor.close()
        conn.close()
        print("DDL scripts executed successfully.")
    else:
        print("Failed to connect to SQL Server.")

if __name__ == "__main__":
    main()
