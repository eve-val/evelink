import os
import tempfile

from tests.compat import unittest

from evelink.cache.sqlite import SqliteCache

class SqliteCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()
        self.cache_path = os.path.join(self.cache_dir, 'sqlite')
        self.cache = SqliteCache(self.cache_path)

    def tearDown(self):
        self.cache.connection.close()
        try:
          os.remove(self.cache_path)
        except OSError:
          pass
        try:
          os.rmdir(self.cache_dir)
        except OSError:
          pass

    def test_cache(self):
        self.cache.put('foo', 'bar', 3600)
        self.cache.put('bar', 1, 3600)
        self.cache.put('baz', True, 3600)
        self.assertEqual(self.cache.get('foo'), 'bar')
        self.assertEqual(self.cache.get('bar'), 1)
        self.assertEqual(self.cache.get('baz'), True)

    def test_expire(self):
        self.cache.put('baz', 'qux', -1)
        self.assertEqual(self.cache.get('baz'), None)
