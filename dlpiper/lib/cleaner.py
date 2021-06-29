from config import config
from main_profile import *
import psycopg2
import re
import time

pattern_name = '<span>(.*)</span></span>'
pattern_url = 'https://www.dlapiper.com(.*)'

def update_data():
    """ update vendor name based on the vendor id """
    sql = """ UPDATE names
                SET name = %s
                WHERE url = %s"""
    try:
        time.sleep(3)
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from names;"
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from names table using cursor.fetchall")
        profile_records = cursor.fetchall()
        print("Print each row and it's columns values")
        for row in profile_records:
            profile_name = str(row[1])
            profile_url = str(row[2])
            result_name = re.search(pattern_name, profile_name)
            result_url = re.search(pattern_url, profile_url)
            if result_name:
                cursor.execute(sql, (str(result_name.group(1)), str(result_url.group(1))))
                connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    update_data()
