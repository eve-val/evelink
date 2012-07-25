import unittest2 as unittest

import mock

import evelink.eve as evelink_eve
from tests.utils import APITestCase

class EVETestCase(APITestCase):

    def setUp(self):
        super(EVETestCase, self).setUp()
        self.eve = evelink_eve.EVE(api=self.api)

    def test_character_names_from_ids(self):
        self.api.get.return_value = self.make_api_result("eve/character_name.xml")

        result = self.eve.character_names_from_ids([1,2])

        self.assertEqual(result, {1:"EVE System", 2:"EVE Central Bank"})
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterName', {'IDs': set([1,2])}),
            ])

    def test_character_name_from_id(self):
        self.api.get.return_value = self.make_api_result("eve/character_name_single.xml")

        result = self.eve.character_name_from_id(1)

        self.assertEqual(result, "EVE System")
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterName', {'IDs': set([1])}),
            ])

    def test_character_ids_from_names(self):
        self.api.get.return_value = self.make_api_result("eve/character_id.xml")

        result = self.eve.character_ids_from_names(["EVE System", "EVE Central Bank"])
        self.assertEqual(result, {"EVE System":1, "EVE Central Bank":2})
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterID', {'names': set(["EVE System","EVE Central Bank"])}),
            ])

    def test_character_id_from_name(self):
        self.api.get.return_value = self.make_api_result("eve/character_id_single.xml")

        result = self.eve.character_id_from_name("EVE System")
        self.assertEqual(result, 1)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/CharacterID', {'names': set(["EVE System"])}),
            ])

    def test_character_info_from_id(self):
        self.api.get.return_value = self.make_api_result("eve/character_info.xml")

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
        self.api.get.return_value = self.make_api_result("eve/alliances.xml")

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
        self.api.get.return_value = self.make_api_result("eve/errors.xml")

        result = self.eve.errors()
        self.assertEqual(result, {1:"Foo", 2:"Bar"})
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/ErrorList'),
            ])

    def test_faction_warfare_stats(self):
        self.api.get.return_value = self.make_api_result("eve/faction_warfare_stats.xml")

        result = self.eve.faction_warfare_stats()
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


    def test_skill_tree(self):
        self.api.get.return_value = self.make_api_result("eve/skill_tree.xml")

        result = self.eve.skill_tree()

        self.assertEqual(result, {
                266: {
                    'id': 266,
                    'name': 'Corporation Management',
                    'skills': {
                        11584 : {
                            'id': 11584,
                            'group_id': 266,
                            'name': 'Anchoring',
                            'description': 'Skill at Anchoring Deployables. Can not be trained on Trial Accounts.',
                            'published': 1,
                            'rank': 3,
                            'primary_attribute': 'memory',
                            'secondary_attribute': 'charisma',
                            'required_skills': {},
                            'bonuses': {
                                'canNotBeTrainedOnTrial': {
                                    'type': 'canNotBeTrainedOnTrial',
                                    'value': 1
                                    }
                                }
                            },

                        3369 : {
                            'id': 3369,
                            'group_id': 266,
                            'name': 'CFO Training',
                            'description': 'Skill at managing corp finances. 5% discount on all fees at non-hostile NPC station if acting as CFO of a corp. ',
                            'published': 0,
                            'rank': 3,
                            'primary_attribute': 'memory',
                            'secondary_attribute': 'charisma',
                            'required_skills': {
                                3363 : { 'id' : 3363, 'level' : 2 },
                                3444 : { 'id' : 3444, 'level' : 3 }
                                },
                            'bonuses': {}
                            }
                        }
                    }
                })

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('eve/SkillTree')
                ])


if __name__ == "__main__":
    unittest.main()
