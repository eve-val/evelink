import mock

from tests.compat import unittest

from evelink.thirdparty.six.moves.urllib.parse import urlparse, parse_qs
import evelink.thirdparty.eve_who as evelink_evewho


class EVEWhoTestCase(unittest.TestCase):

    def test_init(self):
        evewho = evelink_evewho.EVEWho()
        self.assertTrue(isinstance(evewho, evelink_evewho.EVEWho))

    def test_member_list(self):
        mock_fetch = mock.MagicMock()
        mock_fetch.return_value = """
                {"info":{
                    "corporation_id":"869043665",
                    "name":"Woopatang",
                    "member_count":"3"
                    },
                "characters":[
                    {
                    "character_id":"403163173",
                    "corporation_id":"869043665",
                    "alliance_id":"99001433",
                    "name":"Aeryn Tiberius"
                    },
                    {
                    "character_id":"149932493",
                    "corporation_id":"869043665",
                    "alliance_id":"99001433",
                    "name":"Agamemon"
                    },
                    {
                    "character_id":"90464284",
                    "corporation_id":"869043665",
                    "alliance_id":"99001433",
                    "name":"Aidera Boirelle"
                    }
                ]}
            """.strip()

        evewho = evelink_evewho.EVEWho(url_fetch_func=mock_fetch)
        results = evewho._member_list(869043665, 'corplist')

        self.assertEqual(results, [
            {
                'alli_id': 99001433,
                'char_id': 403163173,
                'name': 'Aeryn Tiberius',
                'corp_id': 869043665
            },
            {
                'alli_id': 99001433,
                'char_id': 149932493,
                'name': 'Agamemon',
                'corp_id': 869043665
            },
            {
                'alli_id': 99001433,
                'char_id': 90464284,
                'name': 'Aidera Boirelle',
                'corp_id': 869043665
            }
        ])

        fetch_query_dict = parse_qs(
                urlparse(mock_fetch.mock_calls[0][1][0]).query)
        expected_query_dict = parse_qs('type=corplist&id=869043665&page=0')

        self.assertEqual(fetch_query_dict, expected_query_dict)
