import unittest2 as unittest

from tests.test_appengine import GAEAsyncTestCase

try:
    from evelink.appengine.map import Map
except ImportError:
    pass


class AppEngineEVETestCase(GAEAsyncTestCase):

    def setUp(self):
        super(AppEngineEVETestCase, self).setUp()
        self.client = Map(api=self.api)

    def test_jumps_by_system_async(self):
        self.mock_gets("map/jumps_by_system.xml") 
        self.compare('jumps_by_system')

    def test_kills_by_system_async(self):
        self.mock_gets("map/kills_by_system.xml") 
        self.compare('kills_by_system')

    def test_faction_warfare_systems_async(self):
        self.mock_gets("map/faction_warfare_systems.xml") 
        self.compare('faction_warfare_systems')

    def test_sov_by_system_async(self):
        self.mock_gets("map/sov_by_system.xml") 
        self.compare('sov_by_system')


if __name__ == "__main__":
    unittest.main()
