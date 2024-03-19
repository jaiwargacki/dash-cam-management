""" Module for database connections and operations. 
@author: Jai Wargacki """

import psycopg2

class Database:
    """ Class to handle database connections and operations. """
    def __init__(self, dbname: str = 'dashcam', user: str = 'postgres', host: str = 'localhost', password: str = 'postgres'):
        self.conn = psycopg2.connect(f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def execute(self, query: str):
        """ Execute a query on the database and return the result. """
        self.cur.execute(query)
        return self.cur.fetchall()