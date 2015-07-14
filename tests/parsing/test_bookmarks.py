from tests.compat import unittest
from tests.utils import make_api_result

from evelink.parsing import bookmarks as evelink_b

class BookmarksTestCase(unittest.TestCase):

    def test_parse_bookmarks(self):
        api_result, _, _ = make_api_result("char/bookmarks.xml")

        result = evelink_b.parse_bookmarks(api_result)

        self.assertEqual(result, {
            0: {
                'bookmarks': {
                    12: {
                        'created_ts': 1436391254,
                        'creator_id': 90000001,
                        'id': 12,
                        'item_id': 60014689,
                        'location_id': 30004971,
                        'name': 'Home Station',
                        'note': 'Our base of residence',
                        'type_id': 57,
                        'x': 0.0,
                        'y': 0.0,
                        'z': 0.0,
                    },
                    13: {
                        'created_ts': 1436391307,
                        'creator_id': 90000001,
                        'id': 13,
                        'item_id': 40314792,
                        'location_id': 30004971,
                        'name': 'Sun',
                        'note': '',
                        'type_id': 8,
                        'x': 0.0,
                        'y': 0.0,
                        'z': 0.0,
                    },
                },
                'id': 0,
                'name': '',
            },
            1: {
                'bookmarks': {},
                'id': 1,
                'name': 'A lovely empty folder',
            },
            4: {
                'bookmarks': {
                    14: {
                        'created_ts': 1436391368,
                        'creator_id': 90000001,
                        'id': 14,
                        'item_id': 0,
                        'location_id': 30004971,
                        'name': 'spot in Duripant solar system',
                        'note': '',
                        'type_id': 5,
                        'x': -373405654941.733,
                        'y': 42718621667.0746,
                        'z': -1415023302173.46,
                    },
                },
                'id': 4,
                'name': 'Random crap',
            },
        })
