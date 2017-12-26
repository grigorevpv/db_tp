import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool


class PostgresDataContext(object):

    def __init__(self):
        self._pool = ThreadedConnectionPool(1, -1, database="forums", user="pavel",	password='lomogi99', host='localhost')
        # self._pool = ThreadedConnectionPool(1, -1, database="students", user="postgres", password='lomogi99', host='localhost')

    def _get_connection(self):
        return self._pool.getconn()

    def put_connection(self, conn):
        self._pool.putconn(conn)

    def create_connection(self):
        conn = self._get_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cursor


def connectDB():
    try:
        connect = psycopg2.connect(host="localhost", database="forums", user="pavel", password="lomogi99")
        # connect = psycopg2.connect(host="localhost", database="students", user="postgres", password="lomogi99")
        connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    # finally:
    #     connect.autocommit = True

    return connect
