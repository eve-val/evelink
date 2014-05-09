import mock

from tests.compat import unittest

from tests.test_appengine import (
    GAEAsyncTestCase, auto_test_async_method
)

try:
    from evelink.appengine.account import Account
except ImportError as e:
    Account = mock.Mock()

_specs = ('status','key_info','characters',)


@auto_test_async_method(Account, _specs)
class AppEngineAccountTestCase(GAEAsyncTestCase):
    pass


if __name__ == "__main__":
    unittest.main()
