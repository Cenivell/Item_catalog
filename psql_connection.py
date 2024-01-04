import psycopg2
from psql_connection_config import host, user, db_name, password

try:
    # Connecting to the database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    connection.autocommit = True

except Exception as _ex:
        print("Error while working with PostgreSQL (maybe you should change psql_connection_config file)", _ex)
