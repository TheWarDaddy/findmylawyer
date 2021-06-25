import psycopg2
from config import config

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS names (
            profile_id SERIAL PRIMARY KEY NOT NULL UNIQUE,
            name VARCHAR(255),
            url VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS profiles (
            profile_id SERIAL PRIMARY KEY NOT NULL UNIQUE,
            full_name VARCHAR(8000),
            post VARCHAR(8000),
            post2 VARCHAR(8000),
            email VARCHAR(8000),
            location VARCHAR(8000),
            phoneT VARCHAR(8000),
            related_services VARCHAR(8000),
            related_sectors VARCHAR(8000)
        )
        """,
    )
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

if __name__ == '__main__':
    create_tables()
