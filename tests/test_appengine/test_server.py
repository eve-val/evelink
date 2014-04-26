import mock

from tests.compat import unittest
from tests.test_appengine import (
    GAEAsyncTestCase, auto_test_async_method
)


try:
    from evelink.appengine.server import Server
except ImportError:
    Server = mock.Mock()

@auto_test_async_method(Server, ('server_status',))
class AppEngineServerTestCase(GAEAsyncTestCase):
    pass


if __name__ == "__main__":
    unittest.main()
