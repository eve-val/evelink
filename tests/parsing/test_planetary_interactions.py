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
            1018352222277: {'contents': {},
                            'content': {'type': 0, 'name': '', 'quantity': 0,
                                        'deprecated': 'Use the "contents" field instead'},
                            'cycle_time': 0,
                            'expiry_ts': None,
                            'id': 1018352222277,
                            'install_ts': None,
                            'last_launch_ts': None,
                            'loc': {'lat': 2.30568628105134, 'long': -6.0348096042028},
                            'quantity_per_cycle': 0,
                            'schematic': 0,
                            'type': {'id': 2254, 'name': 'Temperate Command Center'}},
            1018352251143: {'contents': {},
                            'content': {'type': 0, 'name': '', 'quantity': 0,
                                        'deprecated': 'Use the "contents" field instead'},
                            'cycle_time': 30,
                            'expiry_ts': 1433483274,
                            'id': 1018352251143,
                            'install_ts': 1433305074,
                            'last_launch_ts': 1433308674,
                            'loc': {'lat': 2.27884848837, 'long': -5.97671090064},
                            'quantity_per_cycle': 6065,
                            'schematic': 0,
                            'type': {'id': 3068,
                                        'name': 'Temperate Extractor Control Unit'}},
            1018352251145: {'contents': {2268: {'name': 'Aqueous Liquids',
                                                'quantity': 3000,
                                                'type': 2268}},
                            'content': {'name': 'Aqueous Liquids',
                                        'quantity': 3000,
                                        'type': 2268,
                                        'deprecated': 'Use the "contents" field instead'},
                            'cycle_time': 0,
                            'expiry_ts': None,
                            'id': 1018352251145,
                            'install_ts': None,
                            'last_launch_ts': 1433307646,
                            'loc': {'lat': 2.21945171231, 'long': -6.05437394311},
                            'quantity_per_cycle': 0,
                            'schematic': 121,
                            'type': {'id': 2481,
                                        'name': 'Temperate Basic Industry Facility'}},
            1018352251149: {'contents': {2397: {'name': 'Industrial Fibers',
                                                'quantity': 40,
                                                'type': 2397}},
                            'content': {'name': 'Industrial Fibers',
                                        'quantity': 40,
                                        'type': 2397,
                                        'deprecated': 'Use the "contents" field instead'},
                            'cycle_time': 0,
                            'expiry_ts': None,
                            'id': 1018352251149,
                            'install_ts': None,
                            'last_launch_ts': 1433308866,
                            'loc': {'lat': 2.23960260135, 'long': -6.0353691422},
                            'quantity_per_cycle': 0,
                            'schematic': 80,
                            'type': {'id': 2480,
                                        'name': 'Temperate Advanced Industry Facility'}},
            1018352251151: {'contents': {2305: {'name': 'Autotrophs',
                                                'quantity': 160192,
                                                'type': 2305},
                                         9828: {'name': 'Silicon',
                                                'quantity': 2760,
                                                'type': 9828}},
                            'content': {'name': 'Autotrophs',
                                        'quantity': 160192,
                                        'type': 2305,
                                        'deprecated': 'Use the "contents" field instead'},
                            'cycle_time': 0,
                            'expiry_ts': None,
                            'id': 1018352251151,
                            'install_ts': None,
                            'last_launch_ts': None,
                            'loc': {'lat': 2.2437423448, 'long': -6.02030550651},
                            'quantity_per_cycle': 0,
                            'schematic': 0,
                            'type': {'id': 2256, 'name': 'Temperate Launchpad'}},
            1018352251153: {'contents': {2268: {'name': 'Aqueous Liquids',
                                                'quantity': 388209,
                                                'type': 2268},
                                         2397: {'name': 'Industrial Fibers',
                                                'quantity': 2600,
                                                'type': 2397}},
                            'content': {'name': 'Aqueous Liquids',
                                        'quantity': 388209,
                                        'type': 2268,
                                        'deprecated': 'Use the "contents" field instead'},
                            'cycle_time': 0,
                            'expiry_ts': None,
                            'id': 1018352251153,
                            'install_ts': None,
                            'last_launch_ts': 1433308016,
                            'loc': {'lat': 2.25213553747, 'long': -6.03170333208},
                            'quantity_per_cycle': 0,
                            'schematic': 0,
                            'type': {'id': 2562, 'name': 'Temperate Storage Facility'}}
        })
    def test_parse_planetary_routes(self):
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
