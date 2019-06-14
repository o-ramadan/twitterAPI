from psycopg2 import pool


class Database:
    #Class variable: Shared by all objects that have type Database
    #So basically, all Database objects will share this one pool
    __connection_pool = None

    @classmethod
    def initialize(cls,**kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1,
                                                    10,
                                                    **kwargs
                                                    )

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        cls.__connection_pool.closeall()


#Grabs a connection from the connection_pool above
#enter and exit methods are executed at start and end of with
#statement respectively
class CursonFromConnectionPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)
