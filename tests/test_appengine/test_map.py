import mock

from tests.compat import unittest
from tests.test_appengine import (
    GAEAsyncTestCase, auto_test_async_method
)

try:
    from evelink.appengine.map import Map
except ImportError:
    Map = mock.Mock()

@auto_test_async_method(
    Map, 
    (
        'jumps_by_system',
        'kills_by_system',
        'faction_warfare_systems',
        'sov_by_system',
    )
)
class AppEngineMapTestCase(GAEAsyncTestCase):
    pass


if __name__ == "__main__":
    unittest.main()
