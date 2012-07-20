import mock
import unittest2 as unittest

import evelink.char as evelink_char
from tests.utils import APITestCase

class CharTestCase(APITestCase):

    def setUp(self):
        super(CharTestCase, self).setUp()
        self.char = evelink_char.Char(api=self.api)

    def test_wallet_info(self):
        self.api.get.return_value = self.make_api_result("char/wallet_info.xml")

        result = self.char.wallet_info(1)

        self.assertEqual(result, 
            { 
                'balance': 209127923.31,
                'id': 1,
                'key': 1000,
            }
        )
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AccountBalance', {'characterID': 1}),
            ])

    def test_wallet_balance(self):
        self.api.get.return_value = self.make_api_result("char/wallet_balance.xml")

        result = self.char.wallet_balance(1)

        self.assertEqual(result, 209127923.31)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AccountBalance', {'characterID': 1}),
            ])

    def test_industry_jobs(self):
        self.api.get.return_value = self.make_api_result("char/industry_jobs.xml")

        result = self.char.industry_jobs(1)

        self.assertEqual(result, { 
            19962573: {
                'activity_id': 4,                                                                                                 'begin_ts': 1205793300,
                'delivered': False,
                'status': 'failed',
                'finished': False,
                'container_id': 61000139,
                'container_type_id': 21644,
                'end_ts': 1208073300,
                'input': {
                    'id': 178470781,
                    'blueprint_type': 'original',
                    'item_flag': 4,
                    'location_id': 61000139,
                    'mat_level': 0,
                    'prod_level': 0,
                    'quantity': 1,
                    'runs_left': -1,
                    'type_id': 27309},
                'install_ts': 1205423400,
                'system_id': 30002903,
                'installer_id': 975676271,
                'line_id': 100502936,
                'multipliers': {
                    'char_material': 1.25,
                    'char_time': 0.949999988079071,
                    'material': 1.0,
                    'time': 1.0},
                'output': {
                    'bpc_runs': 0,
                    'container_location_id': 30002903,
                    'flag': 0,
                    'location_id': 61000139,
                    'type_id': 27309},
                'runs': 20,
                'pause_ts': None}, 
            37051255: {
                'activity_id': 1,
                'begin_ts': 1233500820,
                'delivered': False,
                'status': 'failed',
                'finished': False,
                'container_id': 61000211,
                'container_type_id': 21644,
                'end_ts': 1233511140,
                'input': {
                    'id': 664432163,
                    'blueprint_type': 'original',
                    'item_flag': 4,
                    'location_id': 61000211,
                    'mat_level': 90,
                    'prod_level': 11,
                    'quantity': 1,
                    'runs_left': -1,
                    'type_id': 894},
                'install_ts': 1233500820,
                'system_id': 30001233,
                'installer_id': 975676271,
                'line_id': 101335750,
                'multipliers': {
                    'char_material': 1.25,
                    'char_time': 0.800000011920929,
                    'material': 1.0,
                    'time': 0.699999988079071},
                'output': {
                    'bpc_runs': 0,
                    'container_location_id': 30001233,
                    'flag': 4,
                    'location_id': 61000211,
                    'type_id': 193},
                'runs': 75,
                'pause_ts': None}
            }
        )
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/IndustryJobs', {'characterID': 1}),
            ])

    def test_kills(self):
        self.api.get.return_value = self.make_api_result("char/kills.xml")

        result = self.char.kills(1)

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
                'items': {
                    2605: {
                        'destroyed': 1,
                        'dropped': 0,
                        'flag': 0,
                        'id': 2605}, 
                    5531: {
                        'destroyed': 0,
                        'dropped': 1,
                        'flag': 0,
                        'id': 5531}, 
                    16273: {
                        'destroyed': 750,
                        'dropped': 0,
                        'flag': 5,
                        'id': 16273}, 
                    21096: {
                        'destroyed': 1,
                        'dropped': 0,
                        'flag': 0,
                        'id': 21096}}, 
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
                'items': {},
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
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/KillLog', {'characterID': 1}),
            ])

    def test_kills_paged(self):
        self.api.get.return_value = self.make_api_result("char/kills_paged.xml")

        self.char.kills(1, 12345)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/KillLog', {'characterID': 1, 'beforeKillID': 12345}),
            ])

    def test_orders(self):
        self.api.get.return_value = self.make_api_result("char/orders.xml")

        result = self.char.orders(1)

        self.assertEqual(result, { 
            2579890411L: {
                'account_key': 1000, 
                'char_id': 91397530,
                'duration': 90,
                'amount': 2120,
                'escrow': 0.0,
                'id': 2579890411L,
                'type': 'sell',
                'timestamp': 1340742712,
                'price': 5100.0,
                'range': 32767,
                'amount_left': 2120,
                'status': 'active',
                'station_id': 60011866,
                'type_id': 3689},
            2584848036L: {
                'account_key': 1000,
                'char_id': 91397530,
                'duration': 90,
                'amount': 1,
                'escrow': 0.0,
                'id': 2584848036L,
                'type': 'sell',
                'timestamp': 1341183080,
                'price': 250000.0,
                'range': 32767,
                'amount_left': 1,
                'status': 'active',
                'station_id': 60012550,
                'type_id': 16399}
            })

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/MarketOrders', {'characterID': 1}),
            ])

    def test_research(self):
        self.api.get.return_value = self.make_api_result("char/research.xml")

        result = self.char.research(1)

        self.assertEqual(result, {
            3014201: {
                'id': 3014201,
                'per_day': 59.52,
                'remaining': -41461.92,
                'skill_id': 11445,
                'timestamp': 1178692470}
            })

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/Research', {'characterID': 1}),
            ])

    def test_current_training(self):
        self.api.get.return_value = self.make_api_result("char/current_training.xml")

        result = self.char.current_training(1)

        self.assertEqual(result, {
            'current_ts': 1291690831,
            'end_sp': 2048000,
            'end_ts': 1295324413,
            'level': 5,
            'start_sp': 362039,
            'start_ts': 1291645953,
            'active': None,
            'type_id': 23950
            })

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/SkillInTraining', {'characterID': 1}),
            ])

    def test_skill_queue(self):
        self.api.get.return_value = self.make_api_result("char/skill_queue.xml")

        result = self.char.skill_queue(1)

        self.assertEqual(result, [
            {
                'end_ts': 1295324413,
                'level': 5,
                'type_id': 23950,
                'start_ts': 1291645953,
                'end_sp': 2048000,
                'start_sp': 362039,
                'position': 0},
            {
                'end_sp': 256000,
                'end_ts': 1342871633,
                'level': 5,
                'position': 1,
                'start_sp': 45255,
                'start_ts': 1342621219,
                'type_id': 3437},
            ])

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/SkillQueue', {'characterID': 1}),
            ])

if __name__ == "__main__":
    unittest.main()
