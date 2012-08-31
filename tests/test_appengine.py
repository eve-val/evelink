import unittest2 as unittest
from google.appengine.ext import testbed

#from StringIO import StringIO

#import mock

from evelink import appengine


class MemcacheCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_cache_memcache(self):
        cache = appengine.AppengineCache()
        cache.put('foo', 'bar', 3600)
        cache.put('bar', 1, 3600)
        cache.put('baz', True, 3600)
        self.assertEqual(cache.get('foo'), 'bar')
        self.assertEqual(cache.get('bar'), 1)
        self.assertEqual(cache.get('baz'), True)

    def test_expire_memcache(self):
        cache = appengine.AppengineCache()
        cache.put('baz', 'qux', -1)
        self.assertEqual(cache.get('baz'), None)


class DatastoreCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_cache_datastore(self):
        cache = appengine.AppengineDatastoreCache()
        cache.put('foo', 'bar', 3600)
        cache.put('bar', 1, 3600)
        cache.put('baz', True, 3600)
        self.assertEqual(cache.get('foo'), 'bar')
        self.assertEqual(cache.get('bar'), 1)
        self.assertEqual(cache.get('baz'), True)

    def test_expire_datastore(self):
        cache = appengine.AppengineDatastoreCache()
        cache.put('baz', 'qux', -1)
        self.assertEqual(cache.get('baz'), None)

if __name__ == "__main__":
    unittest.main()
