DB_NAME = "moodboards"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PASSWORD = "admin"

import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            "dbname='" + DB_NAME + "' user='" + DB_USER + "' host='" + DB_HOST + "' password='" + DB_PASSWORD + "'")

        cursor = conn.cursor()
        cursor.execute("""SELECT name FROM public.images""")
        rows = cursor.fetchall()

        print "\nImages:\n"
        for row in rows:
            print "   ", row[0]

    except:
        print "I am unable to connect to the database"

    return

connect()