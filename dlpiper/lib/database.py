
import psycopg2
import time

hostname = '172.18.0.2:5432'
username = 'postgres'
password = 'tvzygcdiu'
database = 'postgres'

try:
    conn = psycopg2.connect(host='172.18.0.2', user='postgres', port='5432',
                        password='tvzygcdiu', dbname='postgres')
    print("Database connected...")
    time.sleep(2)
    conn.close()
except Exception as DatabaseConnectionRefused:
    print("database Connection Refused")
