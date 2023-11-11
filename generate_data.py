import pyodbc
import random
from datetime import datetime, timedelta
import time

def create_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=sqlserver;'
                          'DATABASE=TestDB;'
                          'UID=sa;'
                          'PWD=Password!123')
    return conn

def insert_order(cursor, order_id, customer_id, item_code, order_date):
    query = '''INSERT INTO Orders (OrderID, CustomerID, ItemCode, OrderDate) 
               VALUES (?, ?, ?, ?)'''
    cursor.execute(query, (order_id, customer_id, item_code, order_date))

def generate_fake_data(rate):
    order_id = 1
    while True:
        customer_id = random.randint(1, 1000)
        item_code = random.randint(100, 999)
        order_date = datetime.now()
        conn = create_connection()
        cursor = conn.cursor()
        insert_order(cursor, order_id, customer_id, item_code, order_date)
        conn.commit()
        conn.close()
        print(f"Inserted OrderID: {order_id}")
        order_id += 1
        time.sleep(rate)

if __name__ == "__main__":
    rate = 1  # orders per second
    generate_fake_data(rate)
