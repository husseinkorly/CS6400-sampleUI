import sys
from loguru import logger
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import pool


# A database class used to connect to the DB and execute queries
class Database:

    _pool = None

    @staticmethod
    def init(config):
        Database._pool = pool.SimpleConnectionPool(1, 10, host=config.DATABASE_HOST,
                                                   user=config.DATABASE_USERNAME,
                                                   password=config.DATABASE_PASSWORD,
                                                   port=config.DATABASE_PORT,
                                                   dbname=config.DATABASE_NAME)

    @staticmethod
    def get_connection():
        return Database._pool.getconn()

    @staticmethod
    def return_connection(conn):
        Database._pool.putconn(conn)


class Cursor:
    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = Database.get_connection()
        self.cur = self.conn.cursor(cursor_factory=DictCursor)

        return self.cur

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_value:
            logger.info(exception_value)
            self.conn.rollback()
        else:
            self.cur.close()
            self.conn.commit()
        Database.return_connection(self.conn)
