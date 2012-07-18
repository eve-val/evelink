import mock

import evelink.char as evelink_char
from tests.utils import APITestCase

class CharTestCase(APITestCase):

    def setUp(self):
        super(CharTestCase, self).setUp()
        self.char = evelink_char.Char(api=self.api)

    def test_wallet_info(self):
        self.api.get.return_value = self.make_api_result(r"""
          <result>
            <rowset name="accounts" key="accountID" columns="accountID,accountKey,balance">
              <row accountID="1" accountKey="1000" balance="209127923.31" />
            </rowset>
          </result>
        """)

        result = self.char.wallet_info(1)

        self.assertEqual(result, 
            { 
                'balance': 209127923.31,
                'id': 1,
                'key': 1000,
            }
        )
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AccountBalance', {'characterID': 1}),
            ])

    def test_wallet_balance(self):
        self.api.get.return_value = self.make_api_result(r"""
          <result>
            <rowset name="accounts" key="accountID" columns="accountID,accountKey,balance">
              <row accountID="1" accountKey="1000" balance="209127923.31" />
            </rowset>
          </result>
        """)

        result = self.char.wallet_balance(1)

        self.assertEqual(result, 209127923.31)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AccountBalance', {'characterID': 1}),
            ])

