from StringIO import StringIO
import unittest2 as unittest

import mock

import evelink.api as evelink_api


class DummyResponse(object):
    def __init__(self, content):
        self.content = content


@unittest.skipIf(not evelink_api._has_requests, '`requests` not available')
class RequestsAPITestCase(unittest.TestCase):

    def setUp(self):
        self.cache = mock.MagicMock(spec=evelink_api.APICache)
        self.api = evelink_api.API(cache=self.cache)

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

        requests_patcher = mock.patch('requests.Session')
        requests_patcher.start()
        import requests
        self.mock_sessions = requests.Session()
        self.requests_patcher = requests_patcher

    def tearDown(self):
        self.requests_patcher.stop()

    def test_raw_get(self):
        self.mock_sessions.post.return_value = DummyResponse(self.test_xml)

        # Pretend we don't have a cached result
        self.cache.get.return_value = None

        tree = self.api.raw_get('foo/Bar', {'a':[1,2,3]})

        result = tree.find('result')
        rowset = result.find('rowset')
        rows = rowset.findall('row')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].attrib['foo'], 'bar')
        self.assertEqual(self.api.last_timestamps, (1255885531, 1258563931))

    @mock.patch('evelink.api.get_ts_value')
    def test_cached_raw_get(self, mock_ts):
        """Make sure that we don't try to call the API if the result is cached."""
        self.mock_sessions.post.return_value = DummyResponse(self.test_xml)
        mock_ts.return_value = 123456
        self.cache.get.return_value = mock.sentinel.cached_result

        result = self.api.raw_get('foo/Bar', {'a':[1,2,3]})

        self.assertEqual(result, mock.sentinel.cached_result)
        self.assertFalse(self.mock_sessions.post.called)
        # timestamp attempted to be extracted.
        self.assertEqual(self.api.last_timestamps, (123456, 123456))

    def test_raw_get_with_apikey(self):
        self.mock_sessions.post.return_value = DummyResponse(self.test_xml)

        api_key = (1, 'code')
        api = evelink_api.API(cache=self.cache, api_key=api_key)

        # Pretend we don't have a cached result
        self.cache.get.return_value = None

        api.raw_get('foo', {'a':[2,3,4]})

        # Make sure the api key id and verification code were passed
        self.assertEqual(self.mock_sessions.post.mock_calls, [
                mock.call(
                    'https://api.eveonline.com/foo.xml.aspx',
                    params='a=2%2C3%2C4&vCode=code&keyID=1',
                ),
            ])

    def test_raw_get_with_error(self):
        self.mock_sessions.get.return_value = DummyResponse(self.error_xml)

        # Pretend we don't have a cached result
        self.cache.get.return_value = None

        self.assertRaises(evelink_api.APIError,
            self.api.raw_get, 'eve/Error')
        self.assertEqual(self.api.last_timestamps, (1255885531, 1258571131))

    def test_cached_get_with_error(self):
        """Make sure that we don't try to call the API if the result is cached."""
        self.mock_sessions.post.return_value = DummyResponse(self.test_xml)
        self.cache.get.return_value = evelink_api.APIError(123, "Foo",
            (1255885531, 1258571131))
        self.assertRaises(evelink_api.APIError,
            self.api.get, 'foo/Bar', {'a':[1,2,3]})

        self.assertFalse(self.mock_sessions.post.called)
        self.assertEqual(self.api.last_timestamps, (1255885531, 1258571131))


if __name__ == "__main__":
    unittest.main()
