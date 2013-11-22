import mock
import unittest2 as unittest

from tests.test_appengine import GAETestCase
from tests.utils import make_api_result

try:
    from google.appengine.ext import ndb
    from evelink.appengine.server import Server
except ImportError:
    pass


class AppEngineServerTestCase(GAETestCase):

    def setUp(self):
        self.server = Server()

    def test_server_status(self):
        future = ndb.Future()
        future.set_result(make_api_result("server/server_status.xml"))
        self.server.api.get_async = mock.create_autospec(
            self.server.api.get_async,
            return_value=future
        )
        result, current, expires = self.server.server_status_async().get_result()

        self.assertEqual(result, {'online':True, 'players':38102})
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)
        self.server.api.get_async.assert_called_once_with('server/ServerStatus')

if __name__ == "__main__":
    unittest.main()
