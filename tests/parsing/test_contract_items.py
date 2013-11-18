import unittest2 as unittest

from tests.utils import make_api_result

from evelink.parsing import contract_items as evelink_c

class ContractItemsTestCase(unittest.TestCase):
    def test_parse_contract_items(self):
        api_result, _, _ = make_api_result("char/contract_items.xml")
        result = evelink_c.parse_contract_items(api_result)
        self.assertEqual(result, [
            {'id': 779703190, 'quantity': 490, 'type_id': 17867, 'action': 'offered', 'singleton': False},
            {'id': 779703191, 'quantity': 60, 'type_id': 17868, 'action': 'offered', 'singleton': False},
            {'id': 779703192, 'quantity': 8360, 'type_id': 1228, 'action': 'offered', 'singleton': False},
            {'id': 779703193, 'quantity': 16617, 'type_id': 1228, 'action': 'offered', 'singleton': False},
        ])

