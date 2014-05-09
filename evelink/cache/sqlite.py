import pickle
import time
import sqlite3

from evelink import api

class SqliteCache(api.APICache):
    """An implementation of APICache using sqlite."""

    def __init__(self, path):
        super(SqliteCache, self).__init__()
        self.connection = sqlite3.connect(path)
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists cache ("key" text primary key on conflict replace,'
                       'value blob, expiration integer)')

    def get(self, key):
        cursor = self.connection.cursor()
        cursor.execute('select value, expiration from cache where "key"=?',(key,))
        result = cursor.fetchone()
        if not result:
            return None
        value, expiration = result
        if expiration < time.time():
            cursor.execute('delete from cache where "key"=?', (key,))
            self.connection.commit()
            return None
        cursor.close()
        return pickle.loads(value)

    def put(self, key, value, duration):
        expiration = time.time() + duration
        value_tuple = (key, sqlite3.Binary(pickle.dumps(value, 2)), expiration)
        cursor = self.connection.cursor()
        cursor.execute('insert into cache values (?, ?, ?)', value_tuple)
        self.connection.commit()
        cursor.close()
