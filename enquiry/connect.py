import psycopg2


def connectDB():

    connect = None

    try:
       connect = conn = psycopg2.connect(host="localhost", database="students", user="pavel", password="lomogi99")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        connect.autocommit = True

    return connect



