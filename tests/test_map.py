import unittest2 as unittest

import mock

from evelink import map as evelink_map
from tests.utils import APITestCase

class MapTestCase(APITestCase):

    def setUp(self):
        super(MapTestCase, self).setUp()
        self.map = evelink_map.Map(api=self.api)

    def test_jumps_by_system(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset name="solarSystems">
                    <row solarSystemID="30001984" shipJumps="10" />
                </rowset>
                <dataTime>2007-12-12 11:50:38</dataTime>
            </result>
        """)

        result = self.map.jumps_by_system()

        self.assertEqual(result, ({30001984:10}, 1197460238))
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('map/Jumps'),
            ])

    def test_kills_by_system(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset name="solarSystems">
                    <row solarSystemID="30001343" shipKills="0" factionKills="17" podKills="0" />
                    <row solarSystemID="30002671" shipKills="1" factionKills="34" podKills="0" />
                    <row solarSystemID="30005327" shipKills="5" factionKills="21" podKills="1" />
                </rowset>
                <dataTime>2007-12-16 10:57:53</dataTime>
            </result>
        """)

        result = self.map.kills_by_system()

        self.assertEqual(result, (
                {
                    30001343: {'id':30001343, 'faction':17, 'ship':0, 'pod':0},
                    30002671: {'id':30002671, 'faction':34, 'ship':1, 'pod':0},
                    30005327: {'id':30005327, 'faction':21, 'ship':5, 'pod':1},
                },
                1197802673,
            ))
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('map/Kills'),
            ])

    def test_faction_warfare_systems(self):
        self.api.get.return_value = self.make_api_result(r"""
            <result>
                <rowset name="solarSystems">
                     <row solarSystemID="30002056" solarSystemName="Resbroko"
                      occupyingFactionID="0" occupyingFactionName="" contested="True" />
                     <row solarSystemID="30002057" solarSystemName="Hadozeko"
                      occupyingFactionID="0" occupyingFactionName="" contested="False" />
                     <row solarSystemID="30003068" solarSystemName="Kourmonen"
                      occupyingFactionID="500002" occupyingFactionName="Minmatar Republic"
                      contested="False" />
                </rowset>
            </result>
        """)

        result = self.map.faction_warfare_systems()

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


if __name__ == "__main__":
    unittest.main()
