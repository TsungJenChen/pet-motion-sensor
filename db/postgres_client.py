import logging
import psycopg2
from db.db_config import *

class PostgresSQL():

    def __init__(self):
        self.config = {'database': DATABASE,
                        'host': HOST,
                        'user': USER,
                        'password': PASSWORD,
                        'port': PORT}


    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname = self.config['database'],
                host = self.config['host'],
                user = self.config['user'],
                password = self.config['password'],
                port= self.config['port'])
            print("Connected Successfully")
        except Exception as e:
            raise e

    def add_record(self, query, data):
        try:
            conn = psycopg2.connect(
                dbname=self.config['database'],
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                port=self.config['port'])
            print("DB Connected Successfully")

            cur = conn.cursor()
            cur.execute(query.format(**data))
            conn.commit()
            conn.close()
            print("DB Connection closed")

        except Exception as e:
            raise e
