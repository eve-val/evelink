import mock
import unittest2 as unittest

import evelink.account as evelink_account
from tests.utils import APITestCase

class AccountTestCase(APITestCase):

    def setUp(self):
        super(AccountTestCase, self).setUp()
        self.account = evelink_account.Account(api=self.api)

    def test_status(self):
        self.api.get.return_value = self.make_api_result("account/status.xml")

        result = self.account.status()

        self.assertEqual(result, {
                'create_ts': 1072915200,
                'logins': 1234,
                'minutes_played': 9999,
                'paid_ts': 1293840000,
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('account/AccountStatus'),
            ])


if __name__ == "__main__":
    unittest.main()
