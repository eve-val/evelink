import time
import sqlite3

from evelink import api

class SQLCache(api.APICache):
    """An implementation of APICache using sqlite."""

    def __init__(self, path):
        super(SQLCache, self).__init__()
        self.connection = sqlite3.connect(path)
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists cache ('
                       '"key" primary key on conflict replace,'
                       'value, expiration integer)')

    def get(self, key):
        cursor = self.connection.cursor()
        cursor.execute('select value, expiration from cache where "key"=?',
                       (key,))
        result = cursor.fetchone()
        if not result:
            return None
        value, expiration = result
        if expiration < time.time():
            cursor.execute('delete from cache where "key"=?', (key,))
            self.connection.commit()
            return None
        cursor.close()
        return value

    def put(self, key, value, duration):
        expiration = time.time() + duration
        value_tuple = (key, value, expiration)
        cursor = self.connection.cursor()
        cursor.execute('insert or replace into cache values (?, ?, ?)',
                       value_tuple)
        self.connection.commit()
        cursor.close()
