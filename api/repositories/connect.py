import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def connectDB():

    try:
       connect = psycopg2.connect(host="localhost", database="students", user="postgres", password="lomogi99")
       connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    # finally:
    #     connect.autocommit = True

    return connect



