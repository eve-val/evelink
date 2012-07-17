import unittest

import mock

import evelink.eve as evelink_eve
from tests.utils import APITestCase

class EVETestCase(APITestCase):

    def setUp(self):
        super(EVETestCase, self).setUp()
        self.eve = evelink_eve.EVE(api=self.api)

    def test_character_names_from_ids(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset>
                    <row characterID="1" name="EVE System" />
                    <row characterID="2" name="EVE Central Bank" />
                </rowset>
            </result>
        """)

        result = self.eve.character_names_from_ids([1,2])

        self.assertEqual(result, {1:"EVE System", 2:"EVE Central Bank"})
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterName', {'IDs': set([1,2])}),
            ])

    def test_character_name_from_id(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset>
                    <row characterID="1" name="EVE System" />
                </rowset>
            </result>
        """)

        result = self.eve.character_name_from_id(1)

        self.assertEqual(result, "EVE System")
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterName', {'IDs': set([1])}),
            ])

    def test_character_ids_from_names(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset>
                    <row characterID="1" name="EVE System" />
                    <row characterID="2" name="EVE Central Bank" />
                </rowset>
            </result>
        """)

        result = self.eve.character_ids_from_names(["EVE System", "EVE Central Bank"])
        self.assertEqual(result, {"EVE System":1, "EVE Central Bank":2})
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterID', {'names': set(["EVE System","EVE Central Bank"])}),
            ])

    def test_character_id_from_name(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset>
                    <row characterID="1" name="EVE System" />
                </rowset>
            </result>
        """)

        result = self.eve.character_id_from_name("EVE System")
        self.assertEqual(result, 1)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterID', {'names': set(["EVE System"])}),
            ])


if __name__ == "__main__":
    unittest.main()
