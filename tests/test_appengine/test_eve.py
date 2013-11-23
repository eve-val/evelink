import unittest2 as unittest

from tests.test_appengine import GAEAsyncTestCase

try:
    from evelink.appengine.eve import EVE
except ImportError:
    pass


class AppEngineEVETestCase(GAEAsyncTestCase):

    def setUp(self):
        super(AppEngineEVETestCase, self).setUp()
        self.client = EVE(api=self.api)

    def test_certificate_tree(self):
        self.mock_gets("eve/certificate_tree.xml") 
        self.compare('certificate_tree')

    def test_character_names_from_ids_async(self):
        self.mock_gets("eve/character_name.xml") 
        self.compare('character_names_from_ids', [1,2])

    def test_character_name_from_id_async(self):
        self.mock_gets("eve/character_name_single.xml") 
        self.compare('character_name_from_id', 1)

    def test_character_ids_from_names_async(self):
        self.mock_gets("eve/character_id.xml") 
        self.compare(
            'character_ids_from_names',
            ["EVE System", "EVE Central Bank"]
        )

    def test_character_id_from_name_async(self):
        self.mock_gets("eve/character_id_single.xml") 
        self.compare('character_id_from_name', "EVE System")

    def test_character_info_from_id_async(self):
        self.mock_gets("eve/character_info.xml") 
        self.compare('character_info_from_id', 1234)

    def test_alliances_async(self):
        self.mock_gets("eve/alliances.xml") 
        self.compare('alliances')

    def test_errors_async(self):
        self.mock_gets("eve/errors.xml") 
        self.compare('errors')

    def test_faction_warfare_stats_async(self):
        self.mock_gets("eve/faction_warfare_stats.xml") 
        self.compare('faction_warfare_stats')

    def test_faction_warfare_leaderboard_async(self):
        self.mock_gets("eve/faction_warfare_leaderboard.xml") 
        self.compare('faction_warfare_leaderboard')

    def test_conquerable_stations_async(self):
        self.mock_gets("eve/conquerable_stations.xml") 
        self.compare('conquerable_stations')

    def test_skill_tree_async(self):
        self.mock_gets("eve/skill_tree.xml") 
        self.compare('skill_tree')

    def test_reference_types_async(self):
        self.mock_gets("eve/reference_types.xml") 
        self.compare('reference_types')


if __name__ == "__main__":
    unittest.main()
