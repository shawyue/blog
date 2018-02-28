# _*- coding:utf-8 _*_

import pymysql.cursors
import time
from logbook import Logger

log = Logger("LIB.MYSQL")

class MySQLClient(object):

    def __init__(self):
        pass
    
    def init_app(self, app):
        self.host = app.config.get("MYSQL_HOST", "127.0.0.1")
        self.port = app.config.get("MYSQL_PORT", 3306)
        self.user = app.config.get("MYSQL_USER", "")
        self.password = app.config.get("MYSQL_PASSWORD", "")
        self.db = app.config.get("MYSQL_DB", "")
        self.charset = app.config.get("MYSQL_CHARSET", "utf8")
        
        return self.connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                                            host=self.host,
                                            port=self.port,
                                            user=self.user,
                                            password=self.password,
                                            db=self.db,
                                            charset=self.charset
                                            )
            self.write_cursor = self.connection.cursor()
            self.read_cursor = self.connection.cursor()
            return  self.connection
        except Exception as e:
            log.error('\n' + str(e) + '\n')
        

    def execute(self, sql, args, cursor = None):

        if(cursor):
            rows = cursor.execute(query=sql, args=args)
        else:
            rows = self.write_cursor.execute(query=sql, args=args)
        return rows

    def execute_many(self, sql, args):
        rows = self.write_cursor.executemany(sql, args)
        return rows

    def fetch_all(self, sql, args = None):
        self.execute(sql=sql, args=args, cursor=self.read_cursor)
        return self.read_cursor.fetchall()

    def fetch_many(self, sql=None, args=None, size=1):
        if(sql):
            self.execute(sql=sql, args=args, cursor=self.read_cursor)
            return self.read_cursor.fetchmany(size)
        else:
            return self.read_cursor.fetchmany(size)

    def fetch_one(self, sql=None, args=None):
        if(sql):
            self.execute(sql=sql, args=args, cursor=self.read_cursor)
            return self.read_cursor.fetchone()
        else:
            return self.read_cursor.fetchone()

    def commit(self):
        return self.connection.commit()

    def rollback(self):
        return self.connection.rollback()

    def begin_transaction(self):
        return self.connection.begin()

    def select_db(self, db):
        self.connection.select_db(db)

    def close_connect(self):
        self.connection.commit()
        self.write_cursor.close()
        self.read_cursor.close()
        self.connection.close()
        return None

    def ping_server(self):
        try:
            self.connection.ping()
        except Exception as e:
            log.error('\n' + str(e) + '\n')
            time.sleep(2)
            self.ping_server()
