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
            profile_id INTEGER NOT NULL UNIQUE,
            CONSTRAINT FK_profile_id FOREIGN KEY (profile_id) REFERENCES names (profile_id),
            full_name VARCHAR(255),
            post VARCHAR(255),
            post2 VARCHAR(255),
            email VARCHAR(255),
            location VARCHAR(255),
            phoneT VARCHAR(255),
            related_services VARCHAR(255),
            related_sectors VARCHAR(255)
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
