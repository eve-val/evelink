import sys
import zlib
import mock
from xml.etree import ElementTree

from tests.compat import unittest

from evelink.thirdparty.six import BytesIO as StringIO
from evelink.thirdparty.six.moves import urllib
import evelink.api as evelink_api

# Python 2.6's ElementTree raises xml.parsers.expat.ExpatError instead
# of ElementTree.ParseError
_xml_error = getattr(ElementTree, 'ParseError', None)
if _xml_error is None:
    import xml.parsers.expat
    _xml_error = xml.parsers.expat.ExpatError

def compress(s):
    return zlib.compress(s)

class HelperTestCase(unittest.TestCase):

    def test_parse_ts(self):
        self.assertEqual(
            evelink_api.parse_ts("2012-06-12 12:04:33"),
            1339502673,
        )

class CacheTestCase(unittest.TestCase):

    def setUp(self):
        self.cache = evelink_api.APICache()

    def test_cache(self):
        self.cache.put('foo', 'bar', 3600)
        self.assertEqual(self.cache.get('foo'), 'bar')

    def test_expire(self):
        self.cache.put('baz', 'qux', -1)
        self.assertEqual(self.cache.get('baz'), None)

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.custom_useragent = 'test UA'
        self.cache = mock.MagicMock(spec=evelink_api.APICache)
        self.api = evelink_api.API(cache=self.cache, user_agent=self.custom_useragent)
        # force disable requests if enabled.
        self._has_requests = evelink_api._has_requests
        evelink_api._has_requests = False

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
            """.strip().encode()

        self.error_xml = r"""
                <?xml version='1.0' encoding='UTF-8'?>
                <eveapi version="2">
                    <currentTime>2009-10-18 17:05:31</currentTime>
                    <error code="123">
                        Test error message.
                    </error>
                    <cachedUntil>2009-11-18 19:05:31</cachedUntil>
                </eveapi>
            """.strip().encode()

    def tearDown(self):
        evelink_api._has_requests = self._has_requests

    def test_cache_key(self):
        assert self.api._cache_key('foo/bar', {})
        assert self.api._cache_key('foo/bar', {'baz': 'qux'})

        self.assertEqual(
            self.api._cache_key('foo/bar', {'a':1, 'b':2}),
            self.api._cache_key('foo/bar', {'b':2, 'a':1}),
        )

    def test_cache_key_variance(self):
        """Make sure that things which shouldn't have the same cache key don't."""
        self.assertNotEqual(
            self.api._cache_key('foo/bar', {'a':1}),
            self.api._cache_key('foo/bar', {'a':2}),
        )

        self.assertNotEqual(
            self.api._cache_key('foo/bar', {'a':1}),
            self.api._cache_key('foo/bar', {'b':1}),
        )

        self.assertNotEqual(
            self.api._cache_key('foo/bar', {}),
            self.api._cache_key('foo/baz', {}),
        )

    def test_cache_key_value(self):
        self.assertEqual(
            "%s-56cdb36bbb5ad30d7d50556509d657d05eae0250" % self.api.CACHE_VERSION,
            self.api._cache_key('foo/bar', {'a':1})
        )

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_get(self, mock_urlopen):
        # mock up an urlopen compatible response object and pretend to have no
        # cached results; similar pattern for all test_get_* methods below.
        mock_urlopen.return_value.read.return_value = self.test_xml
        self.cache.get.return_value = None

        result = self.api.get('foo/Bar', {'a':[1,2,3]})

        self.assertEqual(len(result), 3)
        result, current, expiry = result

        rowset = result.find('rowset')
        rows = rowset.findall('row')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].attrib['foo'], 'bar')
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258563931,
        })
        self.assertEqual(current, 1255885531)
        self.assertEqual(expiry, 1258563931)

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_useragent(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = self.test_xml
        self.cache.get.return_value = None

        self.api.get('foo/Bar', {'a':[1,2,3]})
        test_useragent = '%s %s' % (evelink_api._user_agent, self.custom_useragent)

        self.assertEqual(mock_urlopen.call_args[0][0].headers['User-agent'], test_useragent)

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_cached_get(self, mock_urlopen):
        """Make sure that we don't try to call the API if the result is cached."""
        # mock up a urlopen compatible error response, and pretend to have a
        # good test response cached.
        mock_urlopen.return_value.read.return_value = self.error_xml
        self.cache.get.return_value = self.test_xml

        result = self.api.get('foo/Bar', {'a':[1,2,3]})

        # Ensure this is really not called.
        self.assertFalse(mock_urlopen.called)

        self.assertEqual(len(result), 3)
        result, current, expiry = result

        rowset = result.find('rowset')
        rows = rowset.findall('row')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].attrib['foo'], 'bar')

        # timestamp attempted to be extracted.
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258563931,
        })
        self.assertEqual(current, 1255885531)
        self.assertEqual(expiry, 1258563931)

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_get_with_apikey(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = self.test_xml
        self.cache.get.return_value = None

        api_key = (1, 'code')
        api = evelink_api.API(cache=self.cache, api_key=api_key)

        api.get('foo', {'a':[2,3,4]})

        # Make sure the api key id and verification code were passed
        self.assertTrue(mock_urlopen.called)
        self.assertTrue(len(mock_urlopen.call_args[0]) > 0)

        request = mock_urlopen.call_args[0][0]
        self.assertEqual(
            'https://api.eveonline.com/foo.xml.aspx',
            request.get_full_url()
        )

        request_dict = urllib.parse.parse_qs(request.data.decode())
        expected_request_dict = urllib.parse.parse_qs("a=2%2C3%2C4&vCode=code&keyID=1")

        self.assertEqual(request_dict, expected_request_dict)

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_get_with_error(self, mock_urlopen):
        # I had to go digging in the source code for urllib2 to find out
        # how to manually instantiate HTTPError instances. :( The empty
        # dict is the headers object.
        def raise_http_error(*args, **kw):
            raise urllib.error.HTTPError(
                "http://api.eveonline.com/eve/Error",
                404,
                "Not found!",
                {},
                StringIO(self.error_xml)
            )
        mock_urlopen.side_effect = raise_http_error
        self.cache.get.return_value = None

        self.assertRaises(evelink_api.APIError,
            self.api.get, 'eve/Error')
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258571131,
        })

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_get_with_http_error(self, mock_urlopen):
        def raise_http_error(*args, **kw):
            raise urllib.error.HTTPError(
                "http://api.eveonline.com/eve/Error",
                404,
                "Not found!",
                {},
                StringIO("This was not a nice XML api error.".encode())
            )
        mock_urlopen.side_effect = raise_http_error
        self.cache.get.return_value = None

        self.assertRaises(urllib.error.HTTPError,
            self.api.get, 'eve/Error')

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_get_with_parse_error(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = "Not good xml"
        self.cache.get.return_value = None

        self.assertRaises(_xml_error, self.api.get, 'foo/Bar')

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_get_with_compressed_error(self, mock_urlopen):
        # I had to go digging in the source code for urllib2 to find out
        # how to manually instantiate HTTPError instances. :( The empty
        # dict is the headers object.
        def raise_http_error(*args, **kw):
            raise urllib.error.HTTPError(
                "http://api.eveonline.com/eve/Error",
                404,
                "Not found!",
                {'Content-Encoding': 'gzip'},
                StringIO(compress(self.error_xml))
            )
        mock_urlopen.side_effect = raise_http_error
        self.cache.get.return_value = None

        self.assertRaises(evelink_api.APIError,
            self.api.get, 'eve/Error')
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258571131,
        })

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_cached_get_with_error(self, mock_urlopen):
        """Make sure that we don't try to call the API if the result is cached."""
        # mocked response is good now, with the error response cached.
        mock_urlopen.return_value.read.return_value = self.test_xml
        self.cache.get.return_value = self.error_xml

        self.assertRaises(evelink_api.APIError,
            self.api.get, 'foo/Bar', {'a':[1,2,3]})

        self.assertFalse(mock_urlopen.called)
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258571131,
        })

    @mock.patch('evelink.thirdparty.six.moves.urllib.request.urlopen')
    def test_get_request_compress_response(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = compress(self.test_xml)
        mock_urlopen.return_value.info.return_value.get.return_value = 'gzip'
        self.cache.get.return_value = None

        result = self.api.get('foo/Bar', {'a':[1,2,3]})
        self.assertTrue(mock_urlopen.called)
        self.assertTrue(len(mock_urlopen.call_args[0]) > 0)
        self.assertEqual(
            'gzip',
            mock_urlopen.call_args[0][0].get_header('Accept-encoding')
        )

        self.assertEqual(len(result), 3)
        result, current, expiry = result

        rowset = result.find('rowset')
        rows = rowset.findall('row')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].attrib['foo'], 'bar')
        self.assertEqual(self.api.last_timestamps, {
            'current_time': 1255885531,
            'cached_until': 1258563931,
        })
        self.assertEqual(current, 1255885531)
        self.assertEqual(expiry, 1258563931)

class AutoCallTestCase(unittest.TestCase):

    def test_python_func(self):
        def func(a, b, c=None, d=None):
            return a, b, c, d

        self.assertEqual((1, 2, 3, 4,), func(1, 2, c=3, d=4))
        self.assertEqual((1, 2, 3, 4,), func(a=1, b=2, c=3, d=4))
        self.assertEqual((1, 2, 3, 4,), func(c=3, a=1, b=2, d=4))
        self.assertEqual((1, 2, 3, 4,), func(1, b=2, c=3, d=4))
        self.assertRaises(TypeError, func, 2, a=1, c=3, d=4)

    def test_translate_args(self):
        args = {'foo': 'bar'}
        mapping = {'foo': 'baz'}
        self.assertEqual(
            {'baz': 'bar'},
            evelink_api.translate_args(args, mapping)
        )

    def test_get_args_and_defaults(self):
        def target(a, b, c=None, d=None):
            pass
        args_specs, defaults = evelink_api.get_args_and_defaults(target)
        self.assertEqual(['a', 'b', 'c', 'd'], args_specs)
        self.assertEqual({'c': None, 'd': None}, defaults)

    def test_map_func_args(self):
        args = [1, 2]
        kw = {'c': 3, 'd': 4}
        args_names = ('a', 'b', 'c', 'd',)
        defaults = {'c': None, 'd': None}
        map_ = evelink_api.map_func_args(args, kw, args_names, defaults)
        self.assertEqual({'a': 1, 'b': 2, 'c': 3, 'd': 4}, map_)

    def test_map_func_args_with_default(self):
        args = [1, 2]
        kw = {'c': 3}
        args_names = ('a', 'b', 'c', 'd',)
        defaults = {'c': None, 'd': None}
        map_ = evelink_api.map_func_args(args, kw, args_names, defaults)
        self.assertEqual({'a': 1, 'b': 2, 'c': 3, 'd': None}, map_)

    def test_map_func_args_with_all_positional_arguments(self):
        args = [1, 2, 3, 4]
        kw = {}
        args_names = ('a', 'b', 'c', 'd',)
        defaults = {'c': None, 'd': None}
        map_ = evelink_api.map_func_args(args, kw, args_names, defaults)
        self.assertEqual({'a': 1, 'b': 2, 'c': 3, 'd': 4}, map_)

    def test_map_func_args_with_too_many_argument(self):
        args = [1, 2, 3]
        kw = {'c': 4, 'd': 5}
        args_names = ('a', 'b', 'c', 'd',)
        defaults = {'c': None, 'd': None}
        self.assertRaises(
            TypeError,
            evelink_api.map_func_args,
            args,
            kw,
            args_names,
            defaults
        )

    def test_map_func_args_with_twice_same_argument(self):
        args = [2]
        kw = {'a': 1, 'c': 3, 'd': 4}
        args_names = ('a', 'b', 'c', 'd',)
        defaults = {'c': None, 'd': None}
        self.assertRaises(
            TypeError,
            evelink_api.map_func_args,
            args,
            kw,
            args_names,
            defaults
        )

    def test_map_func_args_with_too_few_args(self):
        args = [1, ]
        kw = {'c': 3, 'd': 4}
        args_names = ('a', 'b', 'c', 'd',)
        defaults = {'c': None, 'd': None}
        self.assertRaises(
            TypeError,
            evelink_api.map_func_args,
            args,
            kw,
            args_names,
            defaults
        )

    def test_deco_add_request_specs(self):

        @evelink_api.auto_call('foo/bar')
        def func(self, char_id, limit=None, before_kill=None, api_result=None):
            pass

        self.assertEqual(
            {
                'path': 'foo/bar',
                'args': [
                    'char_id', 'limit', 'before_kill'
                ],
                'defaults': dict(limit=None, before_kill=None),
                'prop_to_param': tuple(),
                'map_params': {}
            },
            func._request_specs
            )

    def test_call_wrapped_method(self):
        repeat = mock.Mock()
        client = mock.Mock(name='foo')

        @evelink_api.auto_call(
            'foo/bar',
            map_params={'char_id': 'id', 'limit': 'limit', 'before_kill': 'prev'}
        )
        def func(self, char_id, limit=None, before_kill=None, api_result=None):
            repeat(
                self, char_id, limit=limit,
                before_kill=before_kill, api_result=api_result
            )

        func(client, 1, limit=2, before_kill=3)
        repeat.assert_called_once_with(
            client, 1, limit=2, before_kill=3, api_result=client.api.get.return_value
        )
        client.api.get.assert_called_once_with(
            'foo/bar',
            params={'id':1, 'prev': 3, 'limit': 2}
        )

    def test_call_wrapped_method_raise_key_error(self):
        repeat = mock.Mock()
        client = mock.Mock(name='foo')

        @evelink_api.auto_call('foo/bar')
        def func(self, char_id, api_result=None):
            repeat(self, char_id)

        # TODO: raise error when decorating the method
        self.assertRaises(KeyError, func, client, 1)

    def test_call_wrapped_method_none_arguments(self):
        repeat = mock.Mock()
        client = mock.Mock(name='foo')

        @evelink_api.auto_call(
            'foo/bar', map_params={'char_id': 'char_id', 'limit': 'limit'}
        )
        def func(self, char_id, limit=None, api_result=None):
            repeat(self, char_id, limit=limit, api_result=api_result)

        func(client, 1)
        repeat.assert_called_once_with(
            client, 1, limit=None, api_result=client.api.get.return_value
        )
        client.api.get.assert_called_once_with(
            'foo/bar',
            params={'char_id':1}
        )

    def test_call_wrapped_method_with_properties(self):
        repeat = mock.Mock()
        client = mock.Mock(name='client')
        client.char_id = 1

        @evelink_api.auto_call(
            'foo/bar',
            prop_to_param=('char_id',),
            map_params={'char_id': 'char_id', 'limit': 'limit'}
        )
        def func(self, limit=None, api_result=None):
            repeat(
                self,
                limit=limit, api_result=api_result
            )

        func(client, limit=2)
        repeat.assert_called_once_with(
            client, limit=2, api_result=client.api.get.return_value
        )
        client.api.get.assert_called_once_with(
            'foo/bar',
            params={'char_id':1, 'limit': 2}
        )

    def test_call_wrapped_method_with_api_result(self):
        repeat = mock.Mock()
        client = mock.Mock(name='client')
        results = mock.Mock(name='APIResult')

        @evelink_api.auto_call('foo/bar')
        def func(self, char_id, limit=None, before_kill=None, api_result=None):
            repeat(
                self, char_id, limit=limit,
                before_kill=before_kill, api_result=api_result
            )

        func(client, 1, limit=2, before_kill=3, api_result=results)
        repeat.assert_called_once_with(
            client, 1, limit=2, before_kill=3, api_result=results
        )
        self.assertFalse(client.get.called)


if __name__ == "__main__":
    unittest.main()
