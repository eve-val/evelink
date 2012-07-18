import unittest2 as unittest
import mock

import evelink.server as evelink_server
from tests.utils import APITestCase

class ServerTestCase(APITestCase):

    def setUp(self):
        super(ServerTestCase, self).setUp()
        self.server = evelink_server.Server(api=self.api)

    def test_server_status(self):
        self.api.get.return_value = self.make_api_result(r"""
              <result>
                  <serverOpen>True</serverOpen>
                  <onlinePlayers>38102</onlinePlayers>
              </result>
        """)

        result = self.server.server_status()

        self.assertEqual(result, {'online':True, 'players':38102})
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('server/ServerStatus'),
            ])

if __name__ == "__main__":
    unittest.main()
