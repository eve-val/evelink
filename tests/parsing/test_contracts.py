import unittest2 as unittest

from tests.utils import make_api_result

from evelink import api
from evelink.parsing import contracts as evelink_c

class ContractsTestCase(unittest.TestCase):
    def test_parse_contracts(self):
        api_result, _, _ = make_api_result("corp/contracts.xml")
        result = evelink_c.parse_contracts(api_result)
        self.assertEqual(result, {
                5966: {
                    'id': 5966,
                    'issuer': 154416088,
                    'issuer_corp': 154430949,
                    'assignee': 0,
                    'acceptor': 0,
                    'start': 60014659,
                    'end': 60014659,
                    'type': 'ItemExchange',
                    'status': 'Outstanding',
                    'title': '',
                    'corp': False,
                    'availability': 'Public',
                    'issued': api.parse_ts('2010-02-23 11:28:00'),
                    'expired': api.parse_ts('2010-03-24 11:28:00'),
                    'accepted': None,
                    'completed': None,
                    'days': 0,
                    'price': 5000.0,
                    'reward': 0.0,
                    'collateral': 0.0,
                    'buyout': 0.0,
                    'volume': 0.01,
                },
                5968: {
                    'id': 5968,
                    'issuer': 154416088,
                    'issuer_corp': 154430949,
                    'assignee': 154430949,
                    'acceptor': 0,
                    'start': 60003760,
                    'end': 60003760,
                    'type': 'ItemExchange',
                    'status': 'Outstanding',
                    'title': '',
                    'corp': False,
                    'availability': 'Private',
                    'issued': api.parse_ts('2010-02-25 11:33:00'),
                    'expired': api.parse_ts('2010-03-26 11:33:00'),
                    'accepted': None,
                    'completed': None,
                    'days': 0,
                    'price': 0.00,
                    'reward': 0.00,
                    'collateral': 0.00,
                    'buyout': 0.00,
                    'volume': 0.03,
                }
            })
