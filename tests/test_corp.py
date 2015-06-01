import mock

from tests.compat import unittest
from tests.utils import APITestCase

import evelink.api as evelink_api
import evelink.corp as evelink_corp


API_RESULT_SENTINEL = evelink_api.APIResult(mock.sentinel.api_result, 12345, 67890)


class CorpTestCase(APITestCase):

    def setUp(self):
        super(CorpTestCase, self).setUp()
        self.corp = evelink_corp.Corp(api=self.api)

    def test_corporation_sheet_public(self):
        self.api.get.return_value = self.make_api_result("corp/corporation_sheet.xml")

        result, current, expires = self.corp.corporation_sheet(123)

        self.assertEqual(result, {
                'alliance': {'id': 150430947, 'name': 'The Dead Rabbits'},
                'ceo': {'id': 150208955, 'name': 'Mark Roled'},
                'description': "Garth's testing corp of awesome sauce, win sauce as it were. In this\n"
                    "    corp...<br><br>IT HAPPENS ALL OVER",
                'hq': {'id': 60003469,
                       'name': 'Jita IV - Caldari Business Tribunal Information Center'},
                'id': 150212025,
                'logo': {'graphic_id': 0,
                         'shapes': [{'color': 681, 'id': 448},
                                    {'color': 676, 'id': 0},
                                    {'color': 0, 'id': 418}]},
                'members': {'current': 3},
                'name': 'Banana Republic',
                'shares': 1,
                'tax_percent': 93.7,
                'ticker': 'BR',
                'url': 'some url',
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/CorporationSheet', params={'corporationID': 123}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_corporation_sheet(self):
        self.api.get.return_value = self.make_api_result("corp/corporation_sheet.xml")

        result, current, expires = self.corp.corporation_sheet()

        self.assertEqual(result, {
                'alliance': {'id': 150430947, 'name': 'The Dead Rabbits'},
                'ceo': {'id': 150208955, 'name': 'Mark Roled'},
                'description': "Garth's testing corp of awesome sauce, win sauce as it were. In this\n"
                    "    corp...<br><br>IT HAPPENS ALL OVER",
                'hangars': {1000: 'Division 1',
                              1001: 'Division 2',
                              1002: 'Division 3',
                              1003: 'Division 4',
                              1004: 'Division 5',
                              1005: 'Division 6',
                              1006: 'Division 7'},
                'hq': {'id': 60003469,
                       'name': 'Jita IV - Caldari Business Tribunal Information Center'},
                'id': 150212025,
                'logo': {'graphic_id': 0,
                         'shapes': [{'color': 681, 'id': 448},
                                    {'color': 676, 'id': 0},
                                    {'color': 0, 'id': 418}]},
                'members': {'current': 3, 'limit': 6300},
                'name': 'Banana Republic',
                'shares': 1,
                'tax_percent': 93.7,
                'ticker': 'BR',
                'url': 'some url',
                'wallets': {1000: 'Wallet Division 1',
                                     1001: 'Wallet Division 2',
                                     1002: 'Wallet Division 3',
                                     1003: 'Wallet Division 4',
                                     1004: 'Wallet Division 5',
                                     1005: 'Wallet Division 6',
                                     1006: 'Wallet Division 7'}
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/CorporationSheet', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_industry_jobs')
    def test_industry_jobs(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.industry_jobs

        result, current, expires = self.corp.industry_jobs()

        self.assertEqual(result, mock.sentinel.industry_jobs)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/IndustryJobs', params={}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_industry_jobs')
    def test_industry_jobs_history(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.industry_jobs

        result, current, expires = self.corp.industry_jobs_history()

        self.assertEqual(result, mock.sentinel.industry_jobs)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/IndustryJobsHistory', params={}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_npc_standings(self):
        self.api.get.return_value = self.make_api_result("corp/npc_standings.xml")

        result, current, expires = self.corp.npc_standings()

        self.assertEqual(result, {
                'agents': {
                    3008416: {
                        'id': 3008416,
                        'name': 'Antaken Kamola',
                        'standing': 2.71,
                    },
                },
                'corps': {
                    1000003: {
                        'id': 1000003,
                        'name': 'Prompt Delivery',
                        'standing': 0.97,
                    },
                },
                'factions': {
                    500019: {
                        'id': 500019,
                        'name': "Sansha's Nation",
                        'standing': -4.07,
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Standings', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_kills')
    def test_kills(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.kills

        result, current, expires = self.corp.kills()

        self.assertEqual(result, mock.sentinel.kills)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/KillMails', params={}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_kills')
    def test_kill_log(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.kills

        result, current, expires = self.corp.kill_log()

        self.assertEqual(result, mock.sentinel.kills)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/KillLog', params={}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_contract_bids')
    def test_contract_bids(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_contract_bids

        result, current, expires = self.corp.contract_bids()
        self.assertEqual(result, mock.sentinel.parsed_contract_bids)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/ContractBids', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_contract_items')
    def test_contract_items(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_contract_items

        result, current, expires = self.corp.contract_items(12345)
        self.assertEqual(result, mock.sentinel.parsed_contract_items)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/ContractItems', params={'contractID': 12345}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_contracts')
    def test_contracts(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_contracts

        result, current, expires = self.corp.contracts()
        self.assertEqual(result, mock.sentinel.parsed_contracts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Contracts', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_contact_list')
    def test_contacts(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_contacts

        result, current, expires = self.corp.contacts()
        self.assertEqual(result, mock.sentinel.parsed_contacts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/ContactList', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_wallet_info(self):
        self.api.get.return_value = self.make_api_result("corp/wallet_info.xml")

        result, current, expires = self.corp.wallet_info()

        self.assertEqual(result, {
            1000: {'balance': 74171957.08, 'id': 4759, 'key': 1000},
            1001: {'balance': 6.05, 'id': 5687, 'key': 1001},
            1002: {'balance': 0.0, 'id': 5688, 'key': 1002},
            1003: {'balance': 17349111.0, 'id': 5689, 'key': 1003},
            1004: {'balance': 0.0, 'id': 5690, 'key': 1004},
            1005: {'balance': 0.0, 'id': 5691, 'key': 1005},
            1006: {'balance': 0.0, 'id': 5692, 'key': 1006},
        })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/AccountBalance', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_wallet_journal')
    def test_wallet_journal(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_journal

        result, current, expires = self.corp.wallet_journal()
        self.assertEqual(result, mock.sentinel.parsed_journal)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletJournal', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_wallet_journal_paged(self):
        self.api.get.return_value = self.make_api_result("char/wallet_journal.xml")

        self.corp.wallet_journal(before_id=1234)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletJournal', params={'fromID': 1234}),
            ])

    def test_wallet_journal_limit(self):
        self.api.get.return_value = self.make_api_result("char/wallet_journal.xml")

        self.corp.wallet_journal(limit=100)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletJournal', params={'rowCount': 100}),
            ])

    def test_wallet_journal_account_key(self):
        self.api.get.return_value = self.make_api_result("char/wallet_journal.xml")

        self.corp.wallet_journal(account='0003')
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletJournal', params={'accountKey': '0003'}),
            ])

    @mock.patch('evelink.corp.parse_wallet_transactions')
    def test_wallet_transcations(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_transactions

        result, current, expires = self.corp.wallet_transactions()
        self.assertEqual(result, mock.sentinel.parsed_transactions)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletTransactions', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_wallet_transactions_paged(self):
        self.api.get.return_value = self.make_api_result("char/wallet_transactions.xml")

        self.corp.wallet_transactions(before_id=1234)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletTransactions', params={'fromID': 1234}),
            ])

    def test_wallet_transactions_limit(self):
        self.api.get.return_value = self.make_api_result("char/wallet_transactions.xml")

        self.corp.wallet_transactions(limit=100)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletTransactions', params={'rowCount': 100}),
            ])

    def test_wallet_transactions_account_key(self):
        self.api.get.return_value = self.make_api_result("char/wallet_transactions.xml")

        self.corp.wallet_transactions(account='0004')
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletTransactions', params={'accountKey': '0004'}),
            ])

    @mock.patch('evelink.corp.parse_market_orders')
    def test_orders(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_orders

        result, current, expires = self.corp.orders()
        self.assertEqual(result, mock.sentinel.parsed_orders)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MarketOrders', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_faction_warfare_stats(self):
        self.api.get.return_value = self.make_api_result('corp/faction_warfare_stats.xml')

        result, current, expires = self.corp.faction_warfare_stats()

        self.assertEqual(result, {
                'faction': {'id': 500001, 'name': 'Caldari State'},
                'kills': {'total': 0, 'week': 0, 'yesterday': 0},
                'pilots': 6,
                'points': {'total': 0, 'week': 1144, 'yesterday': 0},
                'start_ts': 1213135800,
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/FacWarStats', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.corp.parse_assets')
    def test_assets(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_assets

        result, current, expires = self.corp.assets()
        self.assertEqual(result, mock.sentinel.parsed_assets)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/AssetList', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_shareholders(self):
        self.api.get.return_value = self.make_api_result("corp/shareholders.xml")

        result, current, expires = self.corp.shareholders()

        self.assertEqual(result, {
                'char': {
                    126891489: {
                        'corp': {
                            'id': 632257314,
                            'name': 'Corax.',
                        },
                        'id': 126891489,
                        'name': 'Dragonaire',
                        'shares': 1,
                    },
                },
                'corp': {
                    126891482: {
                        'id': 126891482,
                        'name': 'DragonaireCorp',
                        'shares': 1,
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Shareholders', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_titles(self):
        self.api.get.return_value = self.make_api_result("corp/titles.xml")

        result, current, expires = self.corp.titles()

        self.assertEqual(result, {
                1: {
                    'can_grant': {'at_base': {}, 'at_hq': {}, 'at_other': {}, 'global': {}},
                    'id': 1,
                    'name': 'Member',
                    'roles': {
                        'at_base': {},
                        'at_other': {},
                        'global': {},
                        'at_hq': {
                            8192: {
                                'description': 'Can take items from this divisions hangar',
                                'id': 8192,
                                'name': 'roleHangarCanTake1',
                            },
                        },
                    },
                },
                2: {
                    'can_grant': {'at_base': {}, 'at_hq': {}, 'at_other': {}, 'global': {}},
                    'id': 2,
                    'name': 'unused 1',
                    'roles': {'at_base': {}, 'at_hq': {}, 'at_other': {}, 'global': {}},
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Titles', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_starbases(self):
        self.api.get.return_value = self.make_api_result("corp/starbases.xml")

        result, current, expires = self.corp.starbases()

        self.assertEqual(result, {
                100449451: {
                    'id': 100449451,
                    'location_id': 30000163,
                    'moon_id': 40010395,
                    'online_ts': 1244098851,
                    'standings_owner_id': 673381830,
                    'state': 'online',
                    'state_ts': 1323374621,
                    'type_id': 27538,
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/StarbaseList', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_starbase_details(self):
        self.api.get.return_value = self.make_api_result("corp/starbase_details.xml")

        result, current, expires = self.corp.starbase_details(123)

        self.assertEqual(result, {
                'combat': {
                    'hostility': {
                        'aggression': {'enabled': False},
                        'sec_status': {'enabled': False, 'threshold': 0.0},
                        'standing': {'enabled': True, 'threshold': 9.9},
                        'war': {'enabled': True},
                    },
                    'standings_owner_id': 154683985,
                },
                'fuel': {16274: 18758, 16275: 2447},
                'online_ts': 1240097429,
                'permissions': {
                    'deploy': {
                        'anchor': 'Starbase Config',
                        'offline': 'Starbase Config',
                        'online': 'Starbase Config',
                        'unanchor': 'Starbase Config',
                    },
                    'forcefield': {'alliance': True, 'corp': True},
                    'fuel': {
                        'take': 'Alliance Members',
                        'view': 'Starbase Config',
                    },
                },
                'state': 'online',
                'state_ts': 1241299896,
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/StarbaseDetail', params={'itemID': 123}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_members(self):
        self.api.get.return_value = self.make_api_result("corp/members.xml")

        result, current, expires = self.corp.members()

        self.assertEqual(result, {
                150336922: {
                    'base': {'id': 0, 'name': ''},
                    'can_grant': 0,
                    'id': 150336922,
                    'join_ts': 1181745540,
                    'location': {
                        'id': 60011566,
                        'name': 'Bourynes VII - Moon 2 - University of Caille School',
                    },
                    'logoff_ts': 1182029760,
                    'logon_ts': 1182028320,
                    'name': 'corpexport',
                    'roles': 0,
                    'ship_type': {'id': 606, 'name': 'Velator'},
                    'title': 'asdf',
                },
                150337897: {
                    'base': {'id': 0, 'name': ''},
                    'can_grant': 0,
                    'id': 150337897,
                    'join_ts': 1181826840,
                    'location': {
                        'id': 60011566,
                        'name': 'Bourynes VII - Moon 2 - University of Caille School',
                    },
                    'logoff_ts': 1182029700,
                    'logon_ts': 1182028440,
                    'name': 'corpslave',
                    'roles': 22517998271070336,
                    'ship_type': {'id': 670, 'name': 'Capsule'},
                    'title': '',
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MemberTracking', params={'extended': 1}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_members_not_extended(self):
        self.api.get.return_value = self.make_api_result("corp/members.xml")
        result, current, expires = self.corp.members(extended=False)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MemberTracking', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_permissions(self):
        self.api.get.return_value = self.make_api_result("corp/permissions.xml")

        result, current, expires = self.corp.permissions()

        self.assertEqual(result, {
                123456789: {
                    'can_grant': {
                        'at_base': {4: 'Bar'},
                        'at_hq': {},
                        'at_other': {},
                        'global': {},
                    },
                    'id': 123456789,
                    'name': 'Tester',
                    'roles': {
                        'at_base': {},
                        'at_hq': {},
                        'at_other': {},
                        'global': {1: 'Foo'},
                    },
                    'titles': {
                        1: 'Member ',
                        512: 'Gas Attendant',
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MemberSecurity', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_permissions_log(self):
        self.api.get.return_value = self.make_api_result("corp/permissions_log.xml")

        result, current, expires = self.corp.permissions_log()

        self.assertEqual(result, [
                {
                    'timestamp': 1218131820,
                    'recipient': {'id': 1234567890, 'name': 'Tester'},
                    'roles': {
                        'after': {},
                        'before': {
                            8192: 'roleHangarCanTake1',
                            4398046511104: 'roleContainerCanTake1',
                        },
                    },
                    'role_type': 'at_other',
                    'issuer': {'id': 1234567890, 'name': 'Tester'},
                },
                {
                    'timestamp': 1218131820,
                    'recipient': {'id': 1234567890, 'name': 'Tester'},
                    'roles': {
                        'after': {},
                        'before': {
                            8192: 'roleHangarCanTake1',
                        },
                    },
                    'role_type': 'at_other',
                    'issuer': {'id': 1234567890, 'name': 'Tester'},
                },
                {
                    'timestamp': 1218131820,
                    'recipient': {'id': 1234567890, 'name': 'Tester'},
                    'roles': {
                        'after': {
                            16777216: 'roleHangarCanQuery5',
                        },
                        'before': {},
                    },
                    'role_type': 'at_other',
                    'issuer': {'id': 1234567890, 'name': 'Tester'},
                },
                {
                    'timestamp': 1215452820,
                    'recipient': {'id': 1234567890, 'name': 'Tester'},
                    'roles': {
                        'after': {},
                        'before': {
                            2199023255552: 'roleEquipmentConfig',
                            4503599627370496: 'roleJuniorAccountant',
                        },
                    },
                    'role_type': 'at_other',
                    'issuer': {'id': 1234567890, 'name': 'Tester'},
                },
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MemberSecurityLog', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_stations(self):
        self.api.get.return_value = self.make_api_result("corp/stations.xml")

        result, current, expires = self.corp.stations()

        self.assertEqual(result, {
                61000368: {
                    'docking_fee_per_volume': 0.0,
                    'id': 61000368,
                    'name': 'Station Name Goes Here',
                    'office_fee': 25000000,
                    'owner_id': 857174087,
                    'reprocessing': {'cut': 0.025, 'efficiency': 0.5},
                    'standing_owner_id': 673381830,
                    'system_id': 30004181,
                    'type_id': 21645,
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/OutpostList', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_station_services(self):
        self.api.get.return_value = self.make_api_result("corp/station_services.xml")

        result, current, expires = self.corp.station_services(123)

        self.assertEqual(result, {
                'Market': {
                    'name': 'Market',
                    'owner_id': 857174087,
                    'standing': {
                        'bad_surcharge': 10.0,
                        'good_discount': 0.0,
                        'minimum': 10.0,
                    },
                },
                'Repair Facilities': {
                    'name': 'Repair Facilities',
                    'owner_id': 857174087,
                    'standing': {
                        'bad_surcharge': 10.0,
                        'good_discount': 10.0,
                        'minimum': 10.0,
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/OutpostServiceDetail', params={'itemID': 123}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_medals(self):
        self.api.get.return_value = self.make_api_result("corp/medals.xml")

        result, current, expires = self.corp.medals()

        self.assertEqual(result, {
                1: {
                    'create_ts': 1345740633,
                    'creator_id': 2,
                    'description': 'A test medal.',
                    'id': 1,
                    'title': 'Test Medal',
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Medals', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_member_medals(self):
        self.api.get.return_value = self.make_api_result("corp/member_medals.xml")

        result, current, expires = self.corp.member_medals()

        self.assertEqual(result, {
                1302462525: {
                    24216: {
                        'char_id': 1302462525,
                        'issuer_id': 1824523597,
                        'medal_id': 24216,
                        'public': True,
                        'reason': 'Its True',
                        'timestamp': 1241319835,
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MemberMedals', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_container_log(self):
        self.api.get.return_value = self.make_api_result("corp/container_log.xml")

        result, current, expires = self.corp.container_log()

        self.assertEqual(result, [
                {'action': 'Set Name',
                 'actor': {'id': 783037732, 'name': 'Halo Glory'},
                 'details': {'config': {'new': None, 'old': None},
                             'flag': 4,
                             'password_type': None,
                             'quantity': None,
                             'type_id': None},
                 'item': {'id': 2051471251, 'type_id': 17366},
                 'location_id': 60011728,
                 'timestamp': 1229847000},
                {'action': 'Set Password',
                 'actor': {'id': 783037732, 'name': 'Halo Glory'},
                 'details': {'config': {'new': None, 'old': None},
                             'flag': 4,
                             'password_type': 'Config',
                             'quantity': None,
                             'type_id': None},
                 'item': {'id': 2051471251, 'type_id': 17366},
                 'location_id': 60011728,
                 'timestamp': 1229846940},
                {'action': 'Configure',
                 'actor': {'id': 783037732, 'name': 'Halo Glory'},
                 'details': {'config': {'new': 0, 'old': 0},
                             'flag': 4,
                             'password_type': None,
                             'quantity': None,
                             'type_id': None},
                 'item': {'id': 2051471251, 'type_id': 17366},
                 'location_id': 60011728,
                 'timestamp': 1229846940},
                {'action': 'Assemble',
                 'actor': {'id': 783037732, 'name': 'Halo Glory'},
                 'details': {'config': {'new': None, 'old': None},
                             'flag': 4,
                             'password_type': None,
                             'quantity': None,
                             'type_id': None},
                 'item': {'id': 2051471251, 'type_id': 17366},
                 'location_id': 60011728,
                 'timestamp': 1229846880}
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/ContainerLog', params={}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_locations(self):
        self.api.get.return_value = self.make_api_result("corp/locations.xml")

        result, current, expires = self.corp.locations((1009661446486,1007448817800))
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Locations', params={'IDs': (1009661446486,1007448817800),}),
            ])
        self.assertEqual(result,
            {1009661446486:
                {
                    'id': 1009661446486,
                    'x': None,
                    'z': None,
                    'name': "Superawesome test Impairor",
                    'y': None,
                },
            1007448817800:
                {
                    'id': 1007448817800,
                    'x': -170714848271.291,
                    'z': 208419106396.3,
                    'name': "A Whale",
                    'y': -1728060949.58229,
                }
            }
        )
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_blueprints(self):
        self.api.get.return_value = self.make_api_result("corp/blueprints.xml")

        result, current, expires = self.corp.blueprints()

        self.assertEqual(self.api.mock_calls, [mock.call.get('corp/Blueprints', params={}),])

        self.assertEqual(result, {
                1000000029372: {
                    'location_id': 60014929,
                    'type_id': 11568,
                    'type_name': 'Avatar Blueprint',
                    'location_flag': 4,
                    'quantity': 497,
                    'time_efficiency': 0,
                    'material_efficiency': 0,
                    'runs': -1,
                },
                1000000029377: {
                    'location_id': 60014929,
                    'type_id': 33876,
                    'type_name': 'Prophecy Blood Raiders Edition Blueprint',
                    'location_flag': 4,
                    'quantity': -2,
                    'time_efficiency': 0,
                    'material_efficiency': 0,
                    'runs': 20000,
                },
            })

        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_facilities(self):
        self.api.get.return_value = self.make_api_result("corp/facilities.xml")

        result, current, expires = self.corp.facilities()

        self.assertEqual(self.api.mock_calls, [mock.call.get('corp/Facilities', params={}),])

        self.assertEqual(result, {
                61000936: {
                    'region': {
                        'id': 10000014,
                        'name': 'Catch',
                    },
                    'starbase_modifier': 0.0,
                    'system': {
                        'id': 30001255,
                        'name': 'Y-PNRL',
                    },
                    'tax': 0.0,
                    'type_id': 21644,
                    'type_name': 'Amarr Factory Outpost',
                },
            })

        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_customs_offices(self):
        self.api.get.return_value = self.make_api_result("corp/customsoffices.xml")

        result, current, expires = self.corp.customs_offices()

        self.assertEqual(self.api.mock_calls, [mock.call.get('corp/CustomsOffices', params={}),])

        self.assertEqual(result, {
                1014625297736: {
                    'permissions': {
                        'alliance': True,
                        'standings': True,
                        'minimum_standing': -10.0,
                    },
                    'reinforce_hour': 11,
                    'system': {
                        'id': 30001428,
                        'name': 'Ibura',
                    },
                    'tax_rate': {
                        'alliance': 0.05,
                        'corp': 0.05,
                        'standings': {
                            'high': 0.05,
                            'good': 0.05,
                            'neutral': 0.1,
                            'bad': 0.1,
                            'horrible': 0.1,
                        },
                    },
                },
            })

        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)


if __name__ == "__main__":
    unittest.main()
