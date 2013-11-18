import unittest2 as unittest

import mock

from evelink import map as evelink_map
from tests.utils import APITestCase

class MapTestCase(APITestCase):

    def setUp(self):
        super(MapTestCase, self).setUp()
        self.map = evelink_map.Map(api=self.api)

    def test_jumps_by_system(self):
        self.api.get.return_value = self.make_api_result("map/jumps_by_system.xml")

        (result, data_time), current, expires = self.map.jumps_by_system()

        self.assertEqual(result, {30001984:10})
        self.assertEqual(data_time, 1197460238)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('map/Jumps'),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_kills_by_system(self):
        self.api.get.return_value = self.make_api_result("map/kills_by_system.xml")

        (result, data_time), current, expires = self.map.kills_by_system()

        self.assertEqual(result, {
                30001343: {'id':30001343, 'faction':17, 'ship':0, 'pod':0},
                30002671: {'id':30002671, 'faction':34, 'ship':1, 'pod':0},
                30005327: {'id':30005327, 'faction':21, 'ship':5, 'pod':1},
            })
        self.assertEqual(data_time, 1197802673)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('map/Kills'),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_faction_warfare_systems(self):
        self.api.get.return_value = self.make_api_result("map/faction_warfare_systems.xml")

        result, current, expires = self.map.faction_warfare_systems()

        self.assertEqual(result, {
                30002056: {
                    'contested': True,
                    'faction': {'id': None, 'name': None},
                    'id': 30002056,
                    'name': 'Resbroko',
                },
                30002057: {
                    'contested': False,
                    'faction': {'id': None, 'name': None},
                    'id': 30002057,
                    'name': 'Hadozeko',
                },
                30003068: {
                    'contested': False,
                    'faction': {'id': 500002, 'name': 'Minmatar Republic'},
                    'id': 30003068,
                    'name': 'Kourmonen',
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('map/FacWarSystems'),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_sov_by_system(self):
        self.api.get.return_value = self.make_api_result("map/sov_by_system.xml")

        (result, data_time), current, expires = self.map.sov_by_system()

        self.assertEqual(result, {
                30000480: {
                    'alliance_id': 824518128,
                    'corp_id': 123456789,
                    'faction_id': None,
                    'id': 30000480,
                    'name': '0-G8NO',
                },
                30001597: {
                    'alliance_id': 1028876240,
                    'corp_id': 421957727,
                    'faction_id': None,
                    'id': 30001597,
                    'name': 'M-NP5O',
                },
                30023410: {
                    'alliance_id': None,
                    'corp_id': None,
                    'faction_id': 500002,
                    'id': 30023410,
                    'name': 'Embod',
                },
            })
        self.assertEqual(data_time, 1261545398)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('map/Sovereignty'),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)


if __name__ == "__main__":
    unittest.main()
