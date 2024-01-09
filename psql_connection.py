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
            # If table exists finding out what is the biggest code in the table to generate unique codes
            if table_exists:
                cursor.execute("""SELECT MAX(code) FROM item_catalog;""")
                code = cursor.fetchone()[0]
                # If the table exist but doesn't have any product set the code to 9999999
                if code is None:
                    code = 9999999
            # If the table doesn't exist set the code to 9999999
            else:
                code = 9999999
    except Exception as exc:
        print("Error while checking existence of the table ", exc)

except Exception as _ex:
        print("Error while working with PostgreSQL (maybe you should change psql_connection_config file)", _ex)


