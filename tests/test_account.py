import mock
import unittest2 as unittest

import evelink.account as evelink_account
from evelink import constants
from tests.utils import APITestCase

class AccountTestCase(APITestCase):

    def setUp(self):
        super(AccountTestCase, self).setUp()
        self.account = evelink_account.Account(api=self.api)

    def test_status(self):
        self.api.get.return_value = self.make_api_result("account/status.xml")

        result, current, expires = self.account.status()

        self.assertEqual(result, {
                'create_ts': 1072915200,
                'logins': 1234,
                'minutes_played': 9999,
                'paid_ts': 1293840000,
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('account/AccountStatus'),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_key_info(self):
        self.api.get.return_value = self.make_api_result("account/key_info.xml")

        result, current, expires = self.account.key_info()

        self.assertEqual(result, {
                'access_mask': 59760264,
                'type': constants.CHARACTER,
                'expire_ts': 1315699200,
                'characters': {
                    898901870: {
                        'id': 898901870,
                        'name': "Desmont McCallock",
                        'corp': {
                            'id': 1000009,
                            'name': "Caldari Provisions",
                        },
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('account/APIKeyInfo'),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_characters(self):
        self.api.get.return_value = self.make_api_result("account/characters.xml")

        result, current, expires = self.account.characters()

        self.assertEqual(result, {
                1365215823: {
                    'corp': {
                        'id': 238510404,
                        'name': 'Puppies To the Rescue',
                    },
                    'id': 1365215823,
                    'name': 'Alexis Prey',
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('account/Characters'),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)


if __name__ == "__main__":
    unittest.main()
