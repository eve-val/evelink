import mock

from tests.compat import unittest
from tests.utils import make_api_result

import evelink.parsing.planetary_interactions as evelink_pi

class PlanetaryInteractionsTestCase(unittest.TestCase):

    def test_parse_planetary_colonies(self):
        api_result, _, _ = make_api_result("char/planetary_colonies.xml")
        result = evelink_pi.parse_planetary_colonies(api_result)
        self.assertEqual(result, {
            40223494: {'id': 40223494,
                       'system': {'id': 30003522, 'name': 'Sarum Prime'},
                       'planet': {'name': 'Sarum Prime IV',
                                  'type': 13,
                                  'type_name': 'Planet (Gas)'},
                       'owner': {'id': 1133950739, 'name': 'BarbersHuZ'},
                       'last_update': 1402305835,
                       'upgrade_level': 2,
                       'number_of_pins': 8,
            },
        })

    def test_parse_planetary_links(self):
        api_result, _, _ = make_api_result("char/planetary_links.xml")
        result = evelink_pi.parse_planetary_links(api_result)
        self.assertEqual(result, {
            1014990361645: {'source_id': 1014990361645,
                            'destination_id': 1014990361652,
                            'link_level': 0,
            },
            1014990361646: {'source_id': 1014990361646,
                            'destination_id': 1014990361652,
                            'link_level': 0,
            },
        })

    def test_parse_planetary_pins(self):
        api_result, _, _ = make_api_result("char/planetary_pins.xml")
        result = evelink_pi.parse_planetary_pins(api_result)
        self.assertEqual(result, {
            1014990260630: {'id': 1014990260630,
                            'type': {'id': 2534, 'name': 'Gas Command Center'},
                            'schematic': 0,
                            'last_launch_ts': None,
                            'cycle_time': 0,
                            'quantity_per_cycle': 0,
                            'install_ts': None,
                            'expiry_ts': None,
                            'content': {'type': 0, 'name': '', 'quantity': 0},
                            'loc': {'long': -0.484603382949165,
                                    'lat': -0.484603382949165},
            },
            1014990361645: {'id': 1014990361645,
                            'type': {'id': 3060,
                                     'name': 'Gas Extractor Control Unit',
                            },
                            'schematic': 0,
                            'last_launch_ts': 1402305835,
                            'cycle_time': 15,
                            'quantity_per_cycle': 251,
                            'install_ts': 1402305835,
                            'expiry_ts': 1402392235,
                            'content': {'type': 0, 'name': '', 'quantity': 0},
                            'loc': {'long': -0.461767301597,
                                    'lat': -0.461767301597},
            },
            1014990361650: {'id': 1014990361650,
                            'type': {'id': 2494,
                                     'name': 'Gas Advanced Industry Facility',
                            },
                            'schematic': 69,
                            'last_launch_ts': 1402305835,
                            'cycle_time': 0,
                            'quantity_per_cycle': 0,
                            'install_ts': None,
                            'expiry_ts': None,
                            'content': {'type': 0, 'name': '', 'quantity': 0},
                            'loc': {'long': -0.518403815307,
                                    'lat': -0.518403815307},
            },
            1014990361651: {'id': 1014990361651,
                            'type': {'id': 2543, 'name': 'Gas Launchpad'},
                            'schematic': 0,
                            'last_launch_ts': None,
                            'cycle_time': 0,
                            'quantity_per_cycle': 0,
                            'install_ts': None,
                            'expiry_ts': None,
                            'content': {'type': 0, 'name': '', 'quantity': 0},
                            'loc': {'long': -0.544793681671,
                                    'lat': -0.544793681671},
            },
            1014990361652: {'id': 1014990361652,
                            'type': {'id': 2536, 'name': 'Gas Storage Facility'},
                            'schematic': 0,
                            'last_launch_ts': None,
                            'cycle_time': 0,
                            'quantity_per_cycle': 0,
                            'install_ts': None,
                            'expiry_ts': None,
                            'content': {'type': 0, 'name': '', 'quantity': 0},
                            'loc': {'long': -0.470709152144,
                                    'lat': -0.470709152144},
            },

        })

    def test_parse_planetary_routes(self):
        self.maxDiff=None
        api_result, _, _ = make_api_result("char/planetary_routes.xml")
        result = evelink_pi.parse_planetary_routes(api_result)
        self.assertEqual(result, {
            605707989: {'id': 605707989,
                        'source_id': 1014990361652,
                        'destination_id': 1014990361649,
                        'content': {'type': 2310, 'name': 'Noble Gas'},
                        'quantity': 3000,
                        'path': (1014990361647, 1014990361650, 0, 0, 0),
            },
            605707990: {'id': 605707990,
                        'source_id': 1014990361652,
                        'destination_id': 1014990361647,
                        'content': {'type': 2311, 'name': 'Reactive Gas'},
                        'quantity': 3000,
                        'path': (0, 0, 0, 0, 0),
            },
        })
