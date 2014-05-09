import sys
import mock

from tests.compat import unittest
from tests.utils import make_api_result

try:
    from google.appengine.ext import ndb
except ImportError:
    NO_GAE = True
else:
    from evelink.appengine import AppEngineAPI
    NO_GAE = False


def mock_async_method(class_, method_name, result):
    future = ndb.Future()
    future.set_result(result)
    method = getattr(class_, method_name)
    setattr(
        class_,
        method_name,
        mock.create_autospec(
            method,
            return_value=future
        )
    )

def run_gets(api_wrapper, method_name, src, *args, **kw):
    if kw.get('_client', None) is None:
        api = AppEngineAPI()
        client = api_wrapper(api=api)
    else:
        client = kw.pop('_client')
        api = client.api
    
    raw_resp = make_api_result(src)
    api.get = mock.Mock()
    api.get.return_value = raw_resp
    mock_async_method(api, 'get_async', raw_resp)

    sync = getattr(client, method_name)
    async = getattr(client, '%s_async' % method_name)
    return api, sync(*args, **kw), async(*args, **kw).get_result()    


@unittest.skipIf(sys.version_info[0:2] != (2, 7,), 'GAE requires python 2.7')
@unittest.skipIf(NO_GAE, 'No GAE SDK found')
class GAETestCase(unittest.TestCase):
    """
    Those test cases require python 2.7 and the Google App Engine SDK 
    to be installed.

    """



class auto_test_async_method(object):
    # TODO: should be a metaclass

    def __init__(self, api_wrapper, method_list):
        self.api_wrapper = api_wrapper
        if isinstance(self.api_wrapper, mock.Mock):
            return

        self.method_list = method_list
        self.src_root = api_wrapper.__name__.lower()

    def __call__(self,  cls):
        if isinstance(self.api_wrapper, mock.Mock):
            return cls

        for name in self.method_list:
            src = "%s/%s.xml" % (self.src_root, name)

            setattr(
                cls,
                'test_%s_async' % name, 
                self._make_test(self.api_wrapper, name, src)
            )

        return cls

    def _make_test(self, api_wrapper, method_name, src):
        def test(instance):
            instance.compare(api_wrapper, method_name, src)
        return test


class GAEAsyncTestCase(GAETestCase):
    """Extends GAETestCase to provide helper to test async methods."""

    def compare(self, api_wrapper, method_name, src, *args, **kw):
        api, sync_r, async_r = run_gets(
            api_wrapper, method_name, src, *args, **kw
        )
        self.assertEqual(sync_r, async_r)
        self.assertEqual(1, api.get.call_count)
        self.assertEqual(1, api.get_async.call_count)
        self.assertEqual(api.get.call_args, api.get_async.call_args)

