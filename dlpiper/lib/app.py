from config import config
from main_profile import *
import psycopg2



def app():
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from names;"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from names table using cursor.fetchall")
        profile_records = cursor.fetchall()

        print("Print each row and it's columns values")
        for row in profile_records:
            profile = scrape_infos(row[2])
            cursor.execute("INSERT INTO profiles (profile_id, full_name, post, post2, email, location, phoneT, related_services, related_sectors) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0], profile["full_name"], profile["post"], profile["post2"], profile["email"], profile["location"], profile["phoneT"], profile["related_services"], profile["related_sectors"]))
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    app()
