import mock
import unittest2 as unittest

import evelink.char as evelink_char
from tests.utils import APITestCase

class CharTestCase(APITestCase):

    def setUp(self):
        super(CharTestCase, self).setUp()
        self.char = evelink_char.Char(1, api=self.api)

    @mock.patch('evelink.char.parse_assets')
    def test_assets(self, mock_parse):
        self.api.get.return_value = mock.sentinel.assets_api_result
        mock_parse.return_value = mock.sentinel.parsed_assets

        result = self.char.assets()
        self.assertEqual(result, mock.sentinel.parsed_assets)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.assets_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AssetList', {'characterID': 1}),
            ])

    @mock.patch('evelink.char.parse_contracts')
    def test_contracts(self, mock_parse):
        self.api.get.return_value = mock.sentinel.contracts_api_result
        mock_parse.return_value = mock.sentinel.parsed_contracts

        result = self.char.contracts()
        self.assertEqual(result, mock.sentinel.parsed_contracts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.contracts_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/Contracts', {'characterID': 1}),
            ])

    def test_wallet_journal(self):
        self.api.get.return_value = self.make_api_result("char/wallet_journal.xml")

        result = self.char.wallet_journal()

        self.assertEqual(result, [{
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402941'},
            'balance': 985620165.53,
            'timestamp': 1291962600,
            'id': 3605301231L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        {
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402950'},
            'balance': 985610165.53,
            'timestamp': 1291962600,
            'id': 3605302609L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        {
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402956'},
            'balance': 985600165.53,
            'timestamp': 1291962660,
            'id': 3605303380L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        {
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402974'},
            'balance': 985590165.53,
            'timestamp': 1291962720,
            'id': 3605305292L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        {
            'amount': -10000.0,
            'arg': {'id': 0, 'name': '35402980'},
            'balance': 985580165.53,
            'timestamp': 1291962720,
            'id': 3605306236L,
            'party_1': {'id': 150337897, 'name': 'corpslave12'},
            'party_2': {'id': 1000132, 'name': 'Secure Commerce Commission'},
            'reason': '',
            'tax': {'amount': 0.0, 'taxer_id': 0},
            'type_id': 72},
        ])
        self.assertEqual(self.api.mock_calls, [
            mock.call.get('char/WalletJournal', {'characterID': 1}),
        ])

    def test_wallet_paged(self):
        self.api.get.return_value = self.make_api_result("char/wallet_journal.xml")

        self.char.wallet_journal(before_id=1234)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/WalletJournal', {'characterID': 1, 'fromID': 1234}),
            ])

    def test_wallet_limit(self):
        self.api.get.return_value = self.make_api_result("char/wallet_journal.xml")

        self.char.wallet_journal(limit=100)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/WalletJournal', {'characterID': 1, 'rowCount': 100}),
            ])

    def test_wallet_info(self):
        self.api.get.return_value = self.make_api_result("char/wallet_info.xml")

        result = self.char.wallet_info()

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

        result = self.char.wallet_balance()

        self.assertEqual(result, 209127923.31)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AccountBalance', {'characterID': 1}),
            ])

    @mock.patch('evelink.char.parse_industry_jobs')
    def test_industry_jobs(self, mock_parse):
        self.api.get.return_value = mock.sentinel.industry_jobs_api_result
        mock_parse.return_value = mock.sentinel.industry_jobs

        result = self.char.industry_jobs()

        self.assertEqual(result, mock.sentinel.industry_jobs)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/IndustryJobs', {'characterID': 1}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.industry_jobs_api_result),
            ])

    def test_kills(self):
        self.api.get.return_value = self.make_api_result("char/kills.xml")

        result = self.char.kills()

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

        self.char.kills(12345)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/KillLog', {'characterID': 1, 'beforeKillID': 12345}),
            ])

    def test_character_sheet(self):
        self.api.get.return_value = self.make_api_result("char/character_sheet.xml")

        result = self.char.character_sheet()

        self.assertEqual(result, {
            'id': 150337897,
            'name': 'corpslave',
            'dob': 1136073600,
            'race': 'Minmatar',
            'blood_line': 'Brutor',
            'ancestry': 'Slave Child',
            'gender': 'Female',
            'corp': {
                'id': 150337746,
                'name': 'corpexport Corp',
            },
            'alliance': {
                'id': 0,
                'name': None
            },
            'clone': {
                'name': 'Clone Grade Pi',
                'skill_points': 54600000,
            },
            'balance': 190210393.87,
            'attributes': {
                'charisma': {
                    'base': 7,
                    'bonus': {'bonus': {'name': 'Limited Social Adaptation Chip', 'value': 1}}},
                'intelligence': {
                    'base': 6,
                    'bonus': {'bonus': {'name': 'Snake Delta', 'value': 3}}},
                'memory': {
                    'base': 4,
                    'bonus': {'bonus': {'name': 'Memory Augmentation - Basic', 'value': 3}}},
                'perception': {
                    'base': 12,
                    'bonus': {'bonus': {'name': 'Ocular Filter - Basic', 'value': 3}}},
                'willpower': {
                    'base': 10,
                    'bonus': {'bonus': {'name': 'Neural Boost - Basic', 'value': 3}}}},
        'skills': [{'level': 3, 'published': True, 'skill_points': 8000, 'type': 3431},
                   {'level': 3, 'published': True, 'skill_points': 8000, 'type': 3413},
                   {'level': 1, 'published': True, 'skill_points': 500, 'type': 21059},
                   {'level': 3, 'published': True, 'skill_points': 8000, 'type': 3416},
                   {'level': 5, 'published': False, 'skill_points': 512000, 'type': 3445}],
        'certificates': ['1', '5', '19', '239', '282', '32', '258'],
        'roles': {'Roles': [{'id': 1, 'name': 'roleDirector'}],
                  'RolesAtBase': [{'id': 1, 'name': 'roleDirector'}],
                  'RolesAtHQ': [{'id': 1, 'name': 'roleDirector'}],
                  'RolesAtOther': [{'id': 1, 'name': 'roleDirector'}]},
        'titles': [{'id': 1, 'name': 'Member'}],
        })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/CharacterSheet', {'characterID': 1}),
            ])

    @mock.patch('evelink.char.parse_market_orders')
    def test_orders(self, mock_parse):
        self.api.get.return_value = mock.sentinel.orders_api_result
        mock_parse.return_value = mock.sentinel.parsed_orders

        result = self.char.orders()
        self.assertEqual(result, mock.sentinel.parsed_orders)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.orders_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/MarketOrders', {'characterID': 1}),
            ])

    def test_research(self):
        self.api.get.return_value = self.make_api_result("char/research.xml")

        result = self.char.research()

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

        result = self.char.current_training()

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

        result = self.char.skill_queue()

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

    def test_messages(self):
        self.api.get.return_value = self.make_api_result("char/messages.xml")

        result = self.char.messages()

        self.assertEqual(result, [
                {
                    'id': 290285276,
                    'sender_id': 999999999,
                    'timestamp': 1259629440,
                    'title': 'Corp mail',
                    'to': {
                        'org_id': 999999999,
                        'char_ids': None,
                        'list_ids': None,
                    },
                },
                {
                    'id': 290285275,
                    'sender_id': 999999999,
                    'timestamp': 1259629440,
                    'title': 'Personal mail',
                    'to': {
                        'org_id': None,
                        'char_ids': [999999999],
                        'list_ids': None,
                    },
                },
                {
                    'id': 290285274,
                    'sender_id': 999999999,
                    'timestamp': 1259629440,
                    'title': 'Message to mailing list',
                    'to': {
                        'org_id': None,
                        'char_ids': None,
                        'list_ids': [999999999],
                    },
                },
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/MailMessages', {'characterID': 1}),
            ])


if __name__ == "__main__":
    unittest.main()
