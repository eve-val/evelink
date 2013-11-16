import unittest2 as unittest

from tests.utils import make_api_result

from evelink.parsing import contract_bids as evelink_c

class ContractBidsTestCase(unittest.TestCase):
    def test_parse_contract_bids(self):
        api_result, _, _ = make_api_result("char/contract_bids.xml")
        result = evelink_c.parse_contract_bids(api_result)
        self.assertEqual(result, [
           {'id': 123456,
            'contract_id': 8439234,
            'bidder_id': 984127,
            'timestamp': 1178692470,
            'amount': 1958.12},
           {'id': 4025870,
            'contract_id': 58777338,
            'bidder_id': 91397530,
            'timestamp': 1345698201,
            'amount': 14.0},
        ])


