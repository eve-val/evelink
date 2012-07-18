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
