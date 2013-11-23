import sys
import unittest2 as unittest

import mock

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


@unittest.skipIf(sys.version_info[0:2] != (2, 7,), 'GAE requires python 2.7')
@unittest.skipIf(NO_GAE, 'No GAE SDK found')
class GAETestCase(unittest.TestCase):
    """
    Those test cases require python 2.7 and the Google App Engine SDK 
    to be installed.

    """


class GAEAsyncTestCase(GAETestCase):
    """Extends GAETestCase to provide helper to test async methods."""

    def setUp(self):
        self.client = None
        self.api = AppEngineAPI()
        self.api.get = mock.Mock()

    def mock_gets(self, xml_file_path):
        raw_resp = make_api_result(xml_file_path) 
        self.api.get.return_value = raw_resp
        mock_async_method(self.client.api, 'get_async', raw_resp)

    def compare(self, method_name, *args, **kw):
        sync = getattr(self.client, method_name)
        async = getattr(self.client, '%s_async' %method_name)
        self.assertEqual(sync(*args, **kw), async(*args, **kw).get_result())
        self.assertEqual(1, self.client.api.get.call_count)
        self.assertEqual(1, self.client.api.get_async.call_count)
