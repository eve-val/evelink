import unittest
from xml.etree import ElementTree

import mock

import evelink.api as evelink_api

class APITestCase(unittest.TestCase):
    def setUp(self):
        super(APITestCase, self).setUp()
        self.api = mock.MagicMock(spec=evelink_api.API)

    def make_api_result(self, xml_str):
        return ElementTree.fromstring(xml_str)
