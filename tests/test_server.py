import mock

from tests.compat import unittest
from tests.utils import APITestCase

import evelink.server as evelink_server

class ServerTestCase(APITestCase):

    def setUp(self):
        super(ServerTestCase, self).setUp()
        self.server = evelink_server.Server(api=self.api)

    def test_server_status(self):
        self.api.get.return_value = self.make_api_result("server/server_status.xml")

        result, current, expires = self.server.server_status()

        self.assertEqual(result, {'online':True, 'players':38102})
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('server/ServerStatus', params={}),
            ])

if __name__ == "__main__":
    unittest.main()
