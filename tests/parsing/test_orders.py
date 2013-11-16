import mock
import unittest2 as unittest

from tests.utils import make_api_result

from evelink.parsing import orders as evelink_o

class OrdersTestCase(unittest.TestCase):

    def test_parse_market_orders(self):
        api_result, _, _ = make_api_result("char/orders.xml")

        result = evelink_o.parse_market_orders(api_result)

        self.assertEqual(result, {
            2579890411L: {
                'account_key': 1000,
                'char_id': 91397530,
                'duration': 90,
                'amount': 2120,
                'escrow': 0.0,
                'id': 2579890411L,
                'type': 'sell',
                'timestamp': 1340742712,
                'price': 5100.0,
                'range': 32767,
                'amount_left': 2120,
                'status': 'active',
                'station_id': 60011866,
                'type_id': 3689},
            2584848036L: {
                'account_key': 1000,
                'char_id': 91397530,
                'duration': 90,
                'amount': 1,
                'escrow': 0.0,
                'id': 2584848036L,
                'type': 'sell',
                'timestamp': 1341183080,
                'price': 250000.0,
                'range': 32767,
                'amount_left': 1,
                'status': 'active',
                'station_id': 60012550,
                'type_id': 16399}
            })
