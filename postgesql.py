import psycopg2

def start_connection():
    connection = psycopg2.connect(user="postgres",
                                  password="heslo",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
    return connection, cursor


def finish_connection(connection, cursor):
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        #print("PostgreSQL connection is closed")


def create_table():
    connection, cursor = None, None
    try:
        connection, cursor = start_connection()

        drop_table_query = "DROP TABLE IF EXISTS flats"
        cursor.execute(drop_table_query)
        connection.commit()
        print("Table dropped successfully.")

        create_table_sql = """
                CREATE TABLE flats (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    images TEXT
                )"""
        cursor.execute(create_table_sql)
        connection.commit()
        print("Table was created.")

    except (Exception, psycopg2.Error) as error:
        print("Failed creating table table {}".format(error))

    finally:
        finish_connection(connection, cursor)


def bulk_insert(records):
    connection, cursor = None, None
    try:
        connection, cursor = start_connection()

        sql_insert_query = """ INSERT INTO flats (id, title, images) 
                           VALUES (%s,%s,%s) """

        # executemany() to insert multiple rows
        result = cursor.executemany(sql_insert_query, records)
        connection.commit()
        #print(cursor.rowcount, "Record inserted successfully into flat table")

    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into flat table {}".format(error))

    finally:
        finish_connection(connection, cursor)


def show_table(table_name):
    connection, cursor = None, None
    try:
        connection, cursor = start_connection()
        """create_table_sql = 
                CREATE TABLE flats (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    images TEXT
                )
        cursor.execute(create_table_sql)
        connection.commit()"""
        select_query = "SELECT * FROM {}".format(table_name)
        cursor.execute(select_query)

        rows = cursor.fetchall()
        print("Displaying table")
        for row in rows:
            print(row)

    except (Exception, psycopg2.Error) as error:
        print("Failed while displaying table {}".format(error))

    finally:
        finish_connection(connection, cursor)
        return rows

