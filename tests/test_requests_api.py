import mock
from xml.etree import ElementTree

from tests.compat import unittest

from evelink.thirdparty.six.moves.urllib.parse import parse_qs
import evelink.api as evelink_api

# Python 2.6's ElementTree raises xml.parsers.expat.ExpatError instead
# of ElementTree.ParseError
_xml_error = getattr(ElementTree, 'ParseError', None)
if _xml_error is None:
    import xml.parsers.expat
    _xml_error = xml.parsers.expat.ExpatError

class DummyException(Exception): pass

class DummyResponse(object):
    def __init__(self, content):
        self.status_code = 200
        self.content = content

    def raise_for_status(self):
        if self.status_code != 200:
          raise DummyException("HTTP {0}".format(self.status_code))


@unittest.skipIf(not evelink_api._has_requests, '`requests` not available')
class RequestsAPITestCase(unittest.TestCase):

    def setUp(self):
        self.custom_useragent = 'test UA'
        self.cache = mock.MagicMock(spec=evelink_api.APICache)
        self.api = evelink_api.API(cache=self.cache, user_agent=self.custom_useragent)

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

    def test_get(self):
        # mock up a sessions compatible response object and pretend to have
        # nothing chached; similar pattern below for all test_get_* methods
        self.mock_sessions.post.return_value = DummyResponse(self.test_xml)
        self.cache.get.return_value = None

        tree, current, expires = self.api.get('foo/Bar', {'a':[1,2,3]})

        rowset = tree.find('rowset')
        rows = rowset.findall('row')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].attrib['foo'], 'bar')
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258563931,
        })
        self.assertEqual(current, 1255885531)
        self.assertEqual(expires, 1258563931)

    def test_cached_get(self):
        """Make sure that we don't try to call the API if the result is cached."""
        # mock up a sessions compatible error response, and pretend to have a
        # good test response cached.
        self.mock_sessions.post.return_value = DummyResponse(self.error_xml)
        self.cache.get.return_value = self.test_xml

        result, current, expires = self.api.get('foo/Bar', {'a':[1,2,3]})

        rowset = result.find('rowset')
        rows = rowset.findall('row')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].attrib['foo'], 'bar')

        self.assertFalse(self.mock_sessions.post.called)
        # timestamp attempted to be extracted.
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258563931,
        })
        self.assertEqual(current, 1255885531)
        self.assertEqual(expires, 1258563931)

    def test_get_with_apikey(self):
        self.mock_sessions.post.return_value = DummyResponse(self.test_xml)
        self.cache.get.return_value = None

        api_key = (1, 'code')
        api = evelink_api.API(cache=self.cache, api_key=api_key)

        api.get('foo', {'a':[2,3,4]})

        # Make sure the api key id and verification code were passed
        call_args, call_kwargs = self.mock_sessions.post.mock_calls[0][1:3]
        called_url = call_args[0]
        called_param_dict = call_kwargs["data"]

        expected_url = 'https://api.eveonline.com/foo.xml.aspx'
        expected_param_dict = {'a': '2,3,4', 'vCode': 'code', 'keyID': 1}

        self.assertEqual(called_url, expected_url)
        self.assertEqual(called_param_dict, expected_param_dict)

    def test_useragent(self):
        self.mock_sessions.post.return_value = DummyResponse(self.test_xml)
        self.cache.get.return_value = None

        self.api.get('foo', {'a':[2,3,4]})

        test_useragent = '%s %s' % (evelink_api._user_agent, self.custom_useragent)

        self.assertEqual(self.mock_sessions.headers.update.call_args[0][0]['User-Agent'], test_useragent)

    def test_get_with_error(self):
        self.mock_sessions.get.return_value = DummyResponse(self.error_xml)
        self.cache.get.return_value = None

        self.assertRaises(evelink_api.APIError,
            self.api.get, 'eve/Error')
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258571131,
        })

    def test_get_with_http_error(self):
        self.mock_sessions.get.return_value = DummyResponse("This was not a nice XML api error.")
        self.mock_sessions.get.return_value.status_code = 404
        self.cache.get.return_value = None

        self.assertRaises(DummyException,
            self.api.get, 'eve/Error')

    def test_get_with_parse_error(self):
        self.mock_sessions.get.return_value = DummyResponse("Not nice XML")
        self.mock_sessions.get.return_value.status_code = 200
        self.cache.get.return_value = None

        self.assertRaises(_xml_error,
            self.api.get, 'eve/Error')

    def test_cached_get_with_error(self):
        """Make sure that we don't try to call the API if the result is cached."""
        # mocked response is good now, with the error response cached.
        self.mock_sessions.post.return_value = DummyResponse(self.test_xml)
        self.cache.get.return_value = self.error_xml
        self.assertRaises(evelink_api.APIError,
            self.api.get, 'foo/Bar', {'a':[1,2,3]})

        self.assertFalse(self.mock_sessions.post.called)
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258571131,
        })


if __name__ == "__main__":
    unittest.main()
