import mock

from tests.compat import unittest
from tests.utils import APITestCase

import evelink.account as evelink_account
from evelink import constants

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
                'multi_training_ends': [1418307316, 1418329220],
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('account/AccountStatus', params={}),
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
                        'alliance': None,
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('account/APIKeyInfo', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.api.get.return_value = self.make_api_result("account/key_info_with_alliance.xml")

        result, current, expires = self.account.key_info()
        self.assertEqual(result['characters'][93698525]['alliance'], {
                'id': 99000739,
                'name': "Of Sound Mind",
            })

    def test_characters(self):
        self.api.get.return_value = self.make_api_result("account/characters.xml")

        result, current, expires = self.account.characters()

        self.assertEqual(result, {
                1365215823: {
                    'corp': {
                        'id': 238510404,
                        'name': 'Puppies To the Rescue',
                    },
                    'alliance': None,
                    'id': 1365215823,
                    'name': 'Alexis Prey',
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('account/Characters', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.api.get.return_value = self.make_api_result("account/characters_with_alliance.xml")

        result, current, expires = self.account.characters()

        self.assertEqual(result[93698525]['alliance'], {
                'id': 99000739,
                'name': "Of Sound Mind",
            })


if __name__ == "__main__":
    unittest.main()
