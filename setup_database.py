import pyodbc
import time

def run_ddl_script(cursor, ddl_script):
    with open(ddl_script, 'r') as file:
        ddl_query = file.read()
        cursor.execute(ddl_query)


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
                'PWD=password',
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
        run_ddl_script(cursor, 'ddl.sql')
        cursor.close()
        conn.close()
        print("DDL scripts executed successfully.")
    else:
        print("Failed to connect to SQL Server.")

if __name__ == "__main__":
    main()
