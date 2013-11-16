import mock
import unittest2 as unittest

from tests.utils import make_api_result

from evelink.parsing import contact_list

class ContactsTestCase(unittest.TestCase):
    maxDiff = 1000

    def test_parse_char_contact_list(self):
        api_result, _, _ = make_api_result("char/contact_list.xml")

        result = contact_list.parse_contact_list(api_result)

        expected_result = {
            'corp': {
                1082138174: {'standing': 10.0, 'id': 1082138174,
                             'name': 'Nomad LLP',
                             'in_watchlist': None},
                1086308227: {'standing': 0.0, 'id': 1086308227,
                             'name': 'Rebel Alliance of New Eden',
                             'in_watchlist': None},
                1113838907: {'standing': -10.0, 'id': 1113838907,
                             'name': 'Significant other',
                             'in_watchlist': None}
            },
            'alliance': {
                2049763943: {'standing': -10.0, 'id': 2049763943,
                             'name': 'EntroPraetorian Aegis',
                             'in_watchlist': None},
                2067199408: {'standing': -10.0, 'id': 2067199408,
                             'name': 'Vera Cruz Alliance',
                             'in_watchlist': None},
                2081065875: {'standing': -7.5, 'id': 2081065875,
                             'name': 'TheRedMaple',
                             'in_watchlist': None}
            },
            'personal': {
                3009988: {'standing': 0.0, 'id': 3009988,
                          'name': 'Navittus Sildbena',
                          'in_watchlist': True},
                544497016: {'standing': 10.0, 'id': 544497016,
                            'name': 'Valkyries of Night',
                            'in_watchlist': False}
            }
        }

        self.assertEqual(result['personal'], expected_result['personal'])
        self.assertEqual(result['alliance'], expected_result['alliance'])
        self.assertEqual(result['corp'], expected_result['corp'])
        self.assertEqual(sorted(result.keys()), sorted(expected_result.keys()))

    def test_parse_corp_contact_list(self):
        api_result, _, _ = make_api_result("corp/contact_list.xml")

        result = contact_list.parse_contact_list(api_result)

        expected_result = {
            'corp': {
                1082138174: {'standing': 10.0, 'id': 1082138174,
                             'name': 'Nomad LLP',
                             'in_watchlist': None},
                1086308227: {'standing': 0.0, 'id': 1086308227,
                             'name': 'Rebel Alliance of New Eden',
                             'in_watchlist': None},
                1113838907: {'standing': -10.0, 'id': 1113838907,
                             'name': 'Significant other',
                             'in_watchlist': None}
            },
            'alliance': {
                2049763943: {'standing': -10.0, 'id': 2049763943,
                             'name': 'EntroPraetorian Aegis',
                             'in_watchlist': None},
                2067199408: {'standing': -10.0, 'id': 2067199408,
                             'name': 'Vera Cruz Alliance',
                             'in_watchlist': None},
                2081065875: {'standing': -10.0, 'id': 2081065875,
                             'name': 'TheRedMaple',
                             'in_watchlist': None}
            },
        }

        self.assertEqual(result['alliance'], expected_result['alliance'])
        self.assertEqual(result['corp'], expected_result['corp'])
        self.assertFalse('personal' in result)

        self.assertEqual(sorted(result.keys()), sorted(expected_result.keys()))
