import unittest2 as unittest

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

    def test_character_info_from_id(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <characterID>1234</characterID>
                <characterName>Test Character</characterName>
                <race>Caldari</race>
                <bloodline>Civire</bloodline>
                <corporationID>2345</corporationID>
                <corporation>Test Corporation</corporation>
                <corporationDate>2012-06-03 02:10:00</corporationDate>
                <securityStatus>2.50000000000000</securityStatus>
                <rowset name="employmentHistory">
                    <row corporationID="1" startDate="2012-06-02 02:10:00" />
                    <row corporationID="2" startDate="2011-10-12 12:34:56" />
                </rowset>
            </result>
        """)

        result = self.eve.character_info_from_id(1234)
        self.assertEqual(result, {
            'alliance': {'id': None, 'name': None, 'timestamp': None},
            'bloodline': 'Civire',
            'corp': {'id': 2345, 'name': 'Test Corporation', 'timestamp': 1338689400},
            'history': [
                {'corp_id': '1', 'start_ts': 1338603000},
                {'corp_id': '2', 'start_ts': 1318422896}
            ],
            'id': 1234,
            'isk': None,
            'location': None,
            'name': 'Test Character',
            'race': 'Caldari',
            'sec_status': 2.5,
            'ship': {'name': None, 'type_id': None, 'type_name': None},
            'skillpoints': None,
        })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterInfo', {'characterID': 1234}),
            ])

    def test_alliances(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset name="alliances">
                    <row allianceID="1" executorCorpID="2" memberCount="123"
                     name="Test Alliance" shortName="TEST" startDate="2010-05-01 12:34:00">
                        <rowset name="memberCorporations">
                            <row corporationID="2" startDate="2010-11-08 21:11:00" />
                            <row corporationID="3" startDate="2012-01-28 05:36:00" />
                            <row corporationID="4" startDate="2010-12-15 19:15:00" />
                        </rowset>
                    </row>
                </rowset>
            </result>
        """)

        result = self.eve.alliances()
        self.assertEqual(result, {
                1: {
                    'executor_id': 2,
                    'id': 1,
                    'member_corps': {
                        2: {'id': 2, 'timestamp': 1289250660},
                        3: {'id': 3, 'timestamp': 1327728960},
                        4: {'id': 4, 'timestamp': 1292440500},
                    },
                    'member_count': 123,
                    'name': 'Test Alliance',
                    'ticker': 'TEST',
                    'timestamp': 1272717240,
                }
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/AllianceList'),
            ])


if __name__ == "__main__":
    unittest.main()
