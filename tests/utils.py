import os
import unittest
from xml.etree import ElementTree

import mock

import evelink.api as evelink_api

class APITestCase(unittest.TestCase):
    def setUp(self):
        super(APITestCase, self).setUp()
        self.api = mock.MagicMock(spec=evelink_api.API)

    def make_api_result(self, xml_path):
        xml_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xml')
        with open(os.path.join(xml_dir, xml_path)) as f:
            return ElementTree.parse(f)
