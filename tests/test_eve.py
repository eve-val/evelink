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

    def test_errors(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset name="errors">
                    <row errorCode="1" errorText="Foo" />
                    <row errorCode="2" errorText="Bar" />
                </rowset>
            </result>
        """)

        result = self.eve.errors()
        self.assertEqual(result, {1:"Foo", 2:"Bar"})
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/ErrorList'),
            ])

    def test_faction_warfare_stats(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <totals>
                    <killsYesterday>677</killsYesterday>
                    <killsLastWeek>3246</killsLastWeek>
                    <killsTotal>232772</killsTotal>
                    <victoryPointsYesterday>55087</victoryPointsYesterday>
                    <victoryPointsLastWeek>414049</victoryPointsLastWeek>
                    <victoryPointsTotal>44045189</victoryPointsTotal>
                </totals>
                <rowset name="factions">
                    <row factionID="500001" factionName="Caldari State" pilots="5324"
                        systemsControlled="61" killsYesterday="115" killsLastWeek="627"
                        killsTotal="59239" victoryPointsYesterday="9934" victoryPointsLastWeek="64548"
                        victoryPointsTotal="4506493" />
                    <row factionID="500002" factionName="Minmatar Republic" pilots="4068"
                        systemsControlled="0" killsYesterday="213" killsLastWeek="952"
                        killsTotal="56736" victoryPointsYesterday="2925" victoryPointsLastWeek="51211"
                        victoryPointsTotal="3627522" />
                    <row factionID="500003" factionName="Amarr Empire" pilots="3960"
                        systemsControlled="11" killsYesterday="225" killsLastWeek="1000"
                        killsTotal="55717" victoryPointsYesterday="3330" victoryPointsLastWeek="50518"
                        victoryPointsTotal="3670190" />
                    <row factionID="500004" factionName="Gallente Federation" pilots="3663"
                        systemsControlled="0" killsYesterday="124" killsLastWeek="667"
                        killsTotal="61080" victoryPointsYesterday="10343" victoryPointsLastWeek="62118"
                        victoryPointsTotal="4098366" />
                </rowset>
                <rowset name="factionWars">
                    <row factionID="500001" factionName="Caldari State" againstID="500002"
                        againstName="Minmatar Republic" />
                    <row factionID="500001" factionName="Caldari State" againstID="500004"
                        againstName="Gallente Federation" />
                    <row factionID="500002" factionName="Minmatar Republic" againstID="500001"
                        againstName="Caldari State" />
                    <row factionID="500002" factionName="Minmatar Republic" againstID="500003"
                        againstName="Amarr Empire" />
                    <row factionID="500003" factionName="Amarr Empire" againstID="500002"
                        againstName="Minmatar Republic" />
                    <row factionID="500003" factionName="Amarr Empire" againstID="500004"
                        againstName="Gallente Federation" />
                    <row factionID="500004" factionName="Gallente Federation" againstID="500001"
                        againstName="Caldari State" />
                    <row factionID="500004" factionName="Gallente Federation" againstID="500003"
                        againstName="Amarr Empire" />
                </rowset>
            </result>
        """)

        result = self.eve.faction_warfare_stats()
        from pprint import pprint
        pprint(result)
        self.assertEqual(result, {
            'kills': {'total': 232772, 'week': 3246, 'yesterday': 677},
            'points': {'total': 44045189, 'week': 414049, 'yesterday': 55087},
            'factions': {
                500001: {
                    'id': 500001,
                    'kills': {'total': 59239, 'week': 627, 'yesterday': 115},
                    'name': 'Caldari State',
                    'pilots': 5324,
                    'points': {'total': 4506493, 'week': 64548, 'yesterday': 9934},
                    'systems': 61,
                },
                500002: {
                    'id': 500002,
                    'kills': {'total': 56736, 'week': 952, 'yesterday': 213},
                    'name': 'Minmatar Republic',
                    'pilots': 4068,
                    'points': {'total': 3627522, 'week': 51211, 'yesterday': 2925},
                    'systems': 0,
                },
                500003: {
                    'id': 500003,
                    'kills': {'total': 55717, 'week': 1000, 'yesterday': 225},
                    'name': 'Amarr Empire',
                    'pilots': 3960,
                    'points': {'total': 3670190, 'week': 50518, 'yesterday': 3330},
                    'systems': 11,
                },
                500004: {
                    'id': 500004,
                    'kills': {'total': 61080, 'week': 667, 'yesterday': 124},
                    'name': 'Gallente Federation',
                    'pilots': 3663,
                    'points': {'total': 4098366, 'week': 62118, 'yesterday': 10343},
                    'systems': 0,
                },
            },
            'wars': [
                    {
                        'against': {'id': 500002, 'name': 'Minmatar Republic'},
                        'faction': {'id': 500001, 'name': 'Caldari State'},
                    },
                    {
                        'against': {'id': 500004, 'name': 'Gallente Federation'},
                        'faction': {'id': 500001, 'name': 'Caldari State'},
                    },
                    {
                        'against': {'id': 500001, 'name': 'Caldari State'},
                        'faction': {'id': 500002, 'name': 'Minmatar Republic'},
                    },
                    {
                        'against': {'id': 500003, 'name': 'Amarr Empire'},
                        'faction': {'id': 500002, 'name': 'Minmatar Republic'},
                    },
                    {
                        'against': {'id': 500002, 'name': 'Minmatar Republic'},
                        'faction': {'id': 500003, 'name': 'Amarr Empire'},
                    },
                    {
                        'against': {'id': 500004, 'name': 'Gallente Federation'},
                        'faction': {'id': 500003, 'name': 'Amarr Empire'},
                    },
                    {
                        'against': {'id': 500001, 'name': 'Caldari State'},
                        'faction': {'id': 500004, 'name': 'Gallente Federation'},
                    },
                    {
                        'against': {'id': 500003, 'name': 'Amarr Empire'},
                        'faction': {'id': 500004, 'name': 'Gallente Federation'},
                    }
                ],
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/FacWarStats'),
            ])


if __name__ == "__main__":
    unittest.main()
