import unittest2 as unittest

from tests.utils import make_api_result

from evelink.parsing import assets as evelink_a

class AssetsTestCase(unittest.TestCase):

    def test_parse_assets(self):
        api_result, _, _ = make_api_result("corp/assets.xml")

        result = evelink_a.parse_assets(api_result)

        self.assertEqual(result, {
            30003719: {
                'contents': [
                    {'contents': [
                        {'id': 1007353294812,
                         'item_type_id': 34,
                         'location_flag': 42,
                         'location_id': 30003719,
                         'packaged': True,
                         'quantity': 100},
                        {'id': 1007353294813,
                         'item_type_id': 34,
                         'location_flag': 42,
                         'location_id': 30003719,
                         'packaged': True,
                         'quantity': 200}],
                     'id': 1007222140712,
                     'item_type_id': 16216,
                     'location_flag': 0,
                     'location_id': 30003719,
                     'packaged': False,
                     'quantity': 1}],
                'location_id': 30003719},
            67000050: {
                'contents': [
                    {'id': 1007221285456,
                     'item_type_id': 13780,
                     'location_flag': 0,
                     'location_id': 67000050,
                     'packaged': False,
                     'quantity': 1}],
                'location_id': 67000050}})
