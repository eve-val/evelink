import mock

from tests.compat import unittest

from tests.test_appengine import (
    GAEAsyncTestCase, auto_test_async_method
)

try:
    from evelink.appengine.eve import EVE
except ImportError:
    EVE = mock.Mock()


_specs = (
    'alliances', 
    'errors', 
    'faction_warfare_stats', 
    'faction_warfare_leaderboard', 
    'conquerable_stations', 
    'skill_tree',
    'reference_types',
)


@auto_test_async_method(EVE, _specs)
class AppEngineEVETestCase(GAEAsyncTestCase):

    def test_character_names_from_ids_async(self):
        self.compare(
            EVE,
            'character_names_from_ids',
            "eve/character_name.xml",
            [1,2]
        )

    def test_character_name_from_id_async(self):
        "eve/character_name_single.xml"
        self.compare(
            EVE,
            'character_name_from_id',
            "eve/character_name_single.xml",
            1
        )

    def test_character_ids_from_names_async(self):
        self.compare(
            EVE,
            'character_ids_from_names',
            "eve/character_id.xml",
            ["EVE System", "EVE Central Bank"]
        )

    def test_character_id_from_name_async(self):
        self.compare(
            EVE,
            'character_id_from_name',
            "eve/character_id_single.xml",
            "EVE System"
        )

    def test_character_info_from_id_async(self):
        
        self.compare(
            EVE,
            'character_info_from_id',
            "eve/character_info.xml",
            1234
        )


if __name__ == "__main__":
    unittest.main()
