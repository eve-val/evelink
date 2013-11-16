import unittest2 as unittest

import evelink.parsing.kills as evelink_k
from tests.utils import make_api_result

class KillsTestCase(unittest.TestCase):

    def test_parse_kills(self):
        api_result, _, _ = make_api_result("char/kills.xml")

        result = evelink_k.parse_kills(api_result)

        self.assertEqual(result, {
            15640545: {
                'attackers': {
                    935091361: {
                        'alliance': {
                            'id': 5514808,
                            'name': 'Authorities of EVE'},
                        'corp': {
                            'id': 224588600,
                            'name': 'Inkblot Squad'},
                        'damage': 446,
                        'faction': {
                            'id': 0,
                            'name': ''},
                        'final_blow': True,
                        'id': 935091361,
                        'name': 'ICU123',
                        'sec_status': -0.441287532452161,
                        'ship_type_id': 17932,
                        'weapon_type_id': 2881}},
                'items': [
                    {'destroyed': 0, 'dropped': 1, 'flag': 0, 'id': 5531},
                    {'destroyed': 750, 'dropped': 0, 'flag': 5, 'id': 16273},
                    {'destroyed': 1, 'dropped': 0, 'flag': 0, 'id': 21096},
                    {'destroyed': 1, 'dropped': 0, 'flag': 0, 'id': 2605}],
                'id': 15640545,
                'moon_id': 0,
                'system_id': 30001160,
                'time': 1290612480,
                'victim': {
                    'alliance': {
                        'id': 1254074,
                        'name': 'EVE Gurus'},
                    'corp': {
                        'id': 1254875843,
                        'name': 'Starbase Anchoring Corp'},
                    'damage': 446,
                    'faction': {
                        'id': 0,
                        'name': ''},
                    'id': 150080271,
                    'name': 'Pilot 333',
                    'ship_type_id': 670}},
            15640551: {
                'attackers': {
                    935091361: {
                        'alliance': {
                            'id': 5514808,
                            'name': 'Authorities of EVE'},
                        'corp': {
                            'id': 224588600,
                            'name': 'Inkblot Squad'},
                        'damage': 446,
                        'faction': {
                            'id': 0,
                            'name': ''},
                        'final_blow': True,
                        'id': 935091361,
                        'name': 'ICU123',
                        'sec_status': -0.441287532452161,
                        'ship_type_id': 17932,
                        'weapon_type_id': 2881}},
                'items': [
                    {'destroyed': 1, 'dropped': 0, 'flag': 14, 'id': 1319},
                    {'destroyed': 1, 'dropped': 0, 'flag': 28, 'id': 11370},
                    {'destroyed': 1, 'dropped': 0, 'flag': 93, 'id': 31119},
                    {'destroyed': 1, 'dropped': 0, 'flag': 5, 'id': 3467},
                    {'destroyed': 1, 'dropped': 0, 'flag': 0, 'id': 819},
                    {'destroyed': 2, 'dropped': 0, 'flag': 0, 'id': 4394},
                    {'destroyed': 0, 'dropped': 1, 'flag': 5, 'id': 11489},
                    {'destroyed': 0, 'dropped': 7, 'flag': 0, 'id': 9213},
                    {'destroyed': 0, 'dropped': 1, 'flag': 0, 'id': 4260},
                    {'destroyed': 0, 'dropped': 1, 'flag': 0, 'id': 9141}],
                'id': 15640551,
                'moon_id': 0,
                'system_id': 30001160,
                'time': 1290612540,
                'victim': {
                    'alliance': {
                        'id': 1254074,
                        'name': 'EVE Gurus'},
                    'corp': {
                        'id': 1254875843,
                        'name': 'Starbase Anchoring Corp'},
                    'damage': 446,
                    'faction': {
                        'id': 0,
                        'name': ''},
                    'id': 150080271,
                    'name': 'Pilot 333',
                    'ship_type_id': 670}}
            })
