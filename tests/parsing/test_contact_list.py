import mock
import unittest2 as unittest

from tests.utils import make_api_result

from evelink.parsing import contact_list

class OrdersTestCase(unittest.TestCase):

    def test_parse_char_contact_list(self):
        api_result = make_api_result("char/contact_list.xml")

        result = contact_list.parse_contact_list(api_result)

        expected_result = {
            'corp': {
                1082138174: {'standing': 10, 'id': 1082138174,
                             'name': 'Nomad LLP'},
                1086308227: {'standing': 0, 'id': 1086308227,
                             'name': 'Rebel Alliance of New Eden'},
                1113838907: {'standing': -10, 'id': 1113838907,
                             'name': 'Significant other'}
            },
            'alliance': {
                2049763943: {'standing': -10, 'id': 2049763943,
                             'name': 'EntroPraetorian Aegis'},
                2067199408: {'standing': -10, 'id': 2067199408,
                             'name': 'Vera Cruz Alliance'},
                2081065875: {'standing': -7.5, 'id': 2081065875,
                             'name': 'TheRedMaple'}
            },
            'personal': {
                3009988: {'standing': 0, 'id': 3009988,
                          'name': 'Navittus Sildbena',
                          'in_watchlist': True},
                544497016: {'standing': 10, 'id': 544497016,
                            'name': 'Valkyries of Night',
                            'in_watchlist': False}
            }
        }

        self.assertEqual(result['personal'], expected_result['personal'])
        self.assertEqual(result['alliance'], expected_result['alliance'])
        self.assertEqual(result['corp'], expected_result['corp'])

    def test_parse_corp_contact_list(self):
        api_result = make_api_result("corp/contact_list.xml")

        result = contact_list.parse_contact_list(api_result)

        expected_result = {
            'corp': {
                1082138174: {'standing': 10, 'id': 1082138174,
                             'name': 'Nomad LLP'},
                1086308227: {'standing': 0, 'id': 1086308227,
                             'name': 'Rebel Alliance of New Eden'},
                1113838907: {'standing': -10, 'id': 1113838907,
                             'name': 'Significant other'}
            },
            'alliance': {
                2049763943: {'standing': -10, 'id': 2049763943,
                             'name': 'EntroPraetorian Aegis'},
                2067199408: {'standing': -10, 'id': 2067199408,
                             'name': 'Vera Cruz Alliance'},
                2081065875: {'standing': -10, 'id': 2081065875,
                             'name': 'TheRedMaple'}
            },
        }

        self.assertEqual(result['alliance'], expected_result['alliance'])
        self.assertEqual(result['corp'], expected_result['corp'])
        self.assertFalse('personal' in result)

