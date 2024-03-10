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

    # Checking if the table exists
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'item_catalog');")
            table_exists = cursor.fetchone()[0]
    except Exception as exc:
        print("Error while checking existence of the table ", exc)

except Exception as _ex:
        print("Error while working with PostgreSQL (maybe you should change psql_connection_config file)", _ex)


