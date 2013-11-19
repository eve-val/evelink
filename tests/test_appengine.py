import sys

import mock
import unittest2 as unittest

try:
    from google.appengine.ext import testbed
except ImportError:
    NOGAE = True
else:
    NOGAE = False
    from evelink import appengine


@unittest.skipIf(sys.version_info < (2, 7,), 'GAE requires python 2.7')
@unittest.skipIf(NOGAE, 'No GAE SDK found')
class GAETestCase(unittest.TestCase):
    """
    Those test cases require python 2.6 and the Google App Engine SDK 
    to be installed.

    """


class DatastoreCacheTestCase(GAETestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_cache_datastore(self):
        cache = appengine.AppEngineDatastoreCache()
        cache.put('foo', 'bar', 3600)
        cache.put('bar', 1, 3600)
        cache.put('baz', True, 3600)
        self.assertEqual(cache.get('foo'), 'bar')
        self.assertEqual(cache.get('bar'), 1)
        self.assertEqual(cache.get('baz'), True)

    def test_expire_datastore(self):
        cache = appengine.AppEngineDatastoreCache()
        cache.put('baz', 'qux', -1)
        self.assertEqual(cache.get('baz'), None)


class MemcacheCacheTestCase(GAETestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_cache_memcache(self):
        cache = appengine.AppEngineCache()
        cache.put('foo', 'bar', 3600)
        cache.put('bar', 1, 3600)
        cache.put('baz', True, 3600)
        self.assertEqual(cache.get('foo'), 'bar')
        self.assertEqual(cache.get('bar'), 1)
        self.assertEqual(cache.get('baz'), True)

    def test_expire_memcache(self):
        cache = appengine.AppEngineCache()
        cache.put('baz', 'qux', -1)
        self.assertEqual(cache.get('baz'), None)


class AppEngineAPITestCase(GAETestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()
        self.test_xml = r"""
            <?xml version='1.0' encoding='UTF-8'?>
            <eveapi version="2">
                <currentTime>2009-10-18 17:05:31</currentTime>
                <result>
                    <rowset>
                        <row foo="bar" />
                        <row foo="baz" />
                    </rowset>
                </result>
                <cachedUntil>2009-11-18 17:05:31</cachedUntil>
            </eveapi>
        """.strip()

    @mock.patch('google.appengine.api.urlfetch.fetch')
    def test_get(self, mock_urlfetch):
        mock_urlfetch.return_value.status_code = 200
        mock_urlfetch.return_value.content = self.test_xml

        api = appengine.AppEngineAPI()
        result = api.get('foo/Bar', {'a':[1,2,3]})

        rowset = result.find('rowset')
        rows = rowset.findall('row')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].attrib['foo'], 'bar')
        self.assertEqual(api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258563931,
        })



if __name__ == "__main__":
    unittest.main()
