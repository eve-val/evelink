import mock
from xml.etree import ElementTree

from tests.compat import unittest
from tests.test_appengine import GAETestCase

try:
    from google.appengine.ext import testbed
    from google.appengine.ext import ndb
    from google.appengine.api import apiproxy_stub
    from google.appengine.api import apiproxy_stub_map

except ImportError:
    apiproxy_stub = mock.Mock()
else:

    from evelink import appengine
    from evelink.api import APIError


class URLFetchServiceMock(apiproxy_stub.APIProxyStub):
    """Mock for google.appengine.api.urlfetch.

    http://blog.rebeiro.net/2012/03/mocking-appengines-urlfetch-service-in.html

    """

    def __init__(self, service_name='urlfetch'):
        super(URLFetchServiceMock, self).__init__(service_name)

    def set_return_values(self, **kwargs):
        self.return_values = kwargs

    def _Dynamic_Fetch(self, request, response):
        if type(request.payload()) not in (str,unicode):
            raise TypeError(
                "request.payload() has type %s but expected one of: str, unicode",
                type(request.payload()))
        return_values = self.return_values
        response.set_content(return_values.get('content', ''))
        response.set_statuscode(return_values.get('status_code', 200))
        for header_key, header_value in return_values.get('headers', {}).items():
            new_header = response.add_header()
            new_header.set_key(header_key)
            new_header.set_value(header_value)
        response.set_finalurl(return_values.get('final_url', request.url()))
        response.set_contentwastruncated(return_values.get('content_was_truncated', False))

        self.request = request
        self.response = response


class DatastoreCacheTestCase(GAETestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()
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
        cache.put('baz', 'qux', 3600)
        cache.put('baz', 'qux', -1)
        self.assertEqual(cache.get('baz'), None)

    def test_async_cache(self):
        cache = appengine.AppEngineDatastoreCache()
        ndb.Future.wait_all(
            [
                cache.put_async('foo', 'bar', 3600),
                cache.put_async('bar', 1, 3600),
                cache.put_async('baz', True, 3600),
            ]
        )
        self.assertEqual(cache.get_async('foo').get_result(), 'bar')
        self.assertEqual(cache.get_async('bar').get_result(), 1)
        self.assertEqual(cache.get_async('baz').get_result(), True)


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
        cache.put('baz', 'qux', 3600)
        cache.put('baz', 'qux', -1)
        self.assertEqual(cache.get('baz'), None)

    def test_async_cache(self):
        cache = appengine.AppEngineCache()
        ndb.Future.wait_all(
            [
                cache.put_async('foo', 'bar', 3600),
                cache.put_async('bar', 1, 3600),
                cache.put_async('baz', True, 3600),
            ]
        )
        self.assertEqual(cache.get_async('foo').get_result(), 'bar')
        self.assertEqual(cache.get_async('bar').get_result(), 1)
        self.assertEqual(cache.get_async('baz').get_result(), True)


class AppEngineAPITestCase(GAETestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()
        self.urlfetch_mock = URLFetchServiceMock()
        apiproxy_stub_map.apiproxy.ReplaceStub(
            'urlfetch',
            self.urlfetch_mock
        )

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

        self.error_xml = r"""
            <?xml version='1.0' encoding='UTF-8'?>
            <eveapi version="2">
                <currentTime>2009-10-18 17:05:31</currentTime>
                <error code="123">
                    Test error message.
                </error>
                <cachedUntil>2009-11-18 19:05:31</cachedUntil>
            </eveapi>
        """.strip()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get(self):
        self.urlfetch_mock.set_return_values(
            content=self.test_xml,
            status_code=200
        )

        api = appengine.AppEngineAPI()
        result = api.get('foo/Bar', {'a':[1,2,3]}).result

        rowset = result.find('rowset')
        rows = rowset.findall('row')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].attrib['foo'], 'bar')
        self.assertEqual(api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258563931,
        })

    def test_get_raise_api_error(self):
        self.urlfetch_mock.set_return_values(
            content=self.error_xml,
            status_code=400
        )

        api = appengine.AppEngineAPI()

        self.assertRaises(APIError, api.get, 'eve/Error')
        self.assertEqual(api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258571131,
        })

    def test_get_raise_parse_error(self):
        self.urlfetch_mock.set_return_values(
            content="Not nice XML",
            status_code=200
        )

        api = appengine.AppEngineAPI()

        self.assertRaises(ElementTree.ParseError, api.get, 'eve/Error')

    def test_get_raise_urlfetch_error(self):
        self.urlfetch_mock.set_return_values(
            content="This is not a pretty XML error.",
            status_code=400
        )

        api = appengine.AppEngineAPI()

        self.assertRaises(appengine.api.UrlFetchError, api.get, 'eve/Error')

    def test_get_async(self):
        self.urlfetch_mock.set_return_values(
            content=self.test_xml,
            status_code=200
        )

        api = appengine.AppEngineAPI()
        result = api.get_async('foo/Bar', {'a':[1,2,3]}).get_result().result

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
