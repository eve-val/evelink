import mock
import unittest2 as unittest

import evelink.api as evelink_api
import evelink.char as evelink_char
from tests.utils import APITestCase


API_RESULT_SENTINEL = evelink_api.APIResult(mock.sentinel.api_result, 12345, 67890)


class CharTestCase(APITestCase):

    def setUp(self):
        super(CharTestCase, self).setUp()
        self.char = evelink_char.Char(1, api=self.api)

    @mock.patch('evelink.char.parse_assets')
    def test_assets(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_assets

        result, current, expires = self.char.assets()
        self.assertEqual(result, mock.sentinel.parsed_assets)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AssetList', {'characterID': 1}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.char.parse_contract_bids')
    def test_contract_bids(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_contract_bids

        result, current, expires = self.char.contract_bids()
        self.assertEqual(result, mock.sentinel.parsed_contract_bids)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/ContractBids', {'characterID': 1}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.char.parse_contract_items')
    def test_contract_items(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_contract_items

        result, current, expires = self.char.contract_items(12345)
        self.assertEqual(result, mock.sentinel.parsed_contract_items)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/ContractItems', {'characterID': 1, 'contractID': 12345}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.char.parse_contracts')
    def test_contracts(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_contracts

        result, current, expires = self.char.contracts()
        self.assertEqual(result, mock.sentinel.parsed_contracts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/Contracts', {'characterID': 1}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.char.parse_wallet_journal')
    def test_wallet_journal(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_journal

        result, current, expires = self.char.wallet_journal()
        self.assertEqual(result, mock.sentinel.parsed_journal)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/WalletJournal', {'characterID': 1}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

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

        result, current, expires = self.char.wallet_info()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

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

        result, current, expires = self.char.wallet_balance()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, 209127923.31)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/AccountBalance', {'characterID': 1}),
            ])

    @mock.patch('evelink.char.parse_wallet_transactions')
    def test_wallet_transcations(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_transactions

        result, current, expires = self.char.wallet_transactions()
        self.assertEqual(result, mock.sentinel.parsed_transactions)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/WalletTransactions', {'characterID': 1}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_wallet_transactions_paged(self):
        self.api.get.return_value = self.make_api_result("char/wallet_transactions.xml")

        self.char.wallet_transactions(before_id=1234)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/WalletTransactions', {'characterID': 1, 'fromID': 1234}),
            ])

    def test_wallet_transactions_limit(self):
        self.api.get.return_value = self.make_api_result("char/wallet_transactions.xml")

        self.char.wallet_transactions(limit=100)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/WalletTransactions', {'characterID': 1, 'rowCount': 100}),
            ])

    @mock.patch('evelink.char.parse_industry_jobs')
    def test_industry_jobs(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.industry_jobs

        result, current, expires = self.char.industry_jobs()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, mock.sentinel.industry_jobs)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/IndustryJobs', {'characterID': 1}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])

    @mock.patch('evelink.char.parse_kills')
    def test_kills(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.kills

        result, current, expires = self.char.kills()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, mock.sentinel.kills)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/KillLog', {'characterID': 1}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])

    def test_kills_paged(self):
        self.api.get.return_value = self.make_api_result("char/kills_paged.xml")

        self.char.kills(12345)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/KillLog', {'characterID': 1, 'beforeKillID': 12345}),
            ])

    def test_character_sheet(self):
        self.api.get.return_value = self.make_api_result("char/character_sheet.xml")

        result, current, expires = self.char.character_sheet()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
            'id': 150337897,
            'name': 'corpslave',
            'create_ts': 1136073600,
            'race': 'Minmatar',
            'bloodline': 'Brutor',
            'ancestry': 'Slave Child',
            'gender': 'Female',
            'corp': {
                'id': 150337746,
                'name': 'corpexport Corp',
            },
            'alliance': {
                'id': None,
                'name': None
            },
            'clone': {
                'name': 'Clone Grade Pi',
                'skillpoints': 54600000,
            },
            'balance': 190210393.87,
            'attributes': {
                'charisma': {
                    'base': 7,
                    'total': 8,
                    'bonus': {'name': 'Limited Social Adaptation Chip', 'value': 1}},
                'intelligence': {
                    'base': 6,
                    'total': 9,
                    'bonus': {'name': 'Snake Delta', 'value': 3}},
                'memory': {
                    'base': 4,
                    'total': 7,
                    'bonus': {'name': 'Memory Augmentation - Basic', 'value': 3}},
                'perception': {
                    'base': 12,
                    'total': 15,
                    'bonus': {'name': 'Ocular Filter - Basic', 'value': 3}},
                'willpower': {
                    'base': 10,
                    'total': 13,
                    'bonus': {'name': 'Neural Boost - Basic', 'value': 3}}},
        'skills': [{'level': 3, 'published': True, 'skillpoints': 8000, 'id': 3431},
                   {'level': 3, 'published': True, 'skillpoints': 8000, 'id': 3413},
                   {'level': 1, 'published': True, 'skillpoints': 500, 'id': 21059},
                   {'level': 3, 'published': True, 'skillpoints': 8000, 'id': 3416},
                   {'level': 5, 'published': False, 'skillpoints': 512000, 'id': 3445}],
        'skillpoints': 536500,
        'certificates': set([1, 5, 19, 239, 282, 32, 258]),
        'roles': {'global': {1 : {'id': 1, 'name': 'roleDirector'}},
                  'at_base': {1: {'id': 1, 'name': 'roleDirector'}},
                  'at_hq': {1: {'id': 1, 'name': 'roleDirector'}},
                  'at_other': {1: {'id': 1, 'name': 'roleDirector'}}},
        'titles': {1: {'id': 1, 'name': 'Member'}},
        })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/CharacterSheet', {'characterID': 1}),
            ])

    @mock.patch('evelink.char.parse_contact_list')
    def test_contacts(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_contacts

        result, current, expires = self.char.contacts()
        self.assertEqual(result, mock.sentinel.parsed_contacts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/ContactList', {'characterID': 1}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    @mock.patch('evelink.char.parse_market_orders')
    def test_orders(self, mock_parse):
        self.api.get.return_value = API_RESULT_SENTINEL
        mock_parse.return_value = mock.sentinel.parsed_orders

        result, current, expires = self.char.orders()
        self.assertEqual(result, mock.sentinel.parsed_orders)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/MarketOrders', {'characterID': 1}),
            ])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_notifications(self):
        self.api.get.return_value = self.make_api_result("char/notifications.xml")

        result, current, expires = self.char.notifications()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
            303795523: {'id': 303795523,
                        'read': True,
                        'sender_id': 671216635,
                        'timestamp': 1270836240,
                        'type_id': 16},
            304084087: {'id': 304084087,
                        'read': False,
                        'sender_id': 797400947,
                        'timestamp': 1271075520,
                        'type_id': 16}
            })

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/Notifications', {'characterID': 1}),
            ])

    def test_notification_texts(self):
        self.api.get.return_value = self.make_api_result("char/notification_texts.xml")

        result, current, expires = self.char.notification_texts(1234)
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
            374044083: {'shipTypeID': 606,
                        'id': 374044083,
                        'isHouseWarmingGift': 1},
            374067406: {'dueDate': 1336342200L,
                        'amount': 25000000,
                        'id': 374067406},
            374106507: {'cost': None,
                        'declaredByID': 98105019,
                        'delayHours': None,
                        'hostileState': None,
                        'againstID': 673381830,
                        'id': 374106507},
            374119034: {'aggressorCorpID': 785714366,
                        'aggressorID': 1746208390,
                        'armorValue': 1.0,
                        'hullValue': 1.0,
                        'moonID': 40264916,
                        'shieldValue': 0.995,
                        'solarSystemID': 30004181,
                        'typeID': 16688,
                        'aggressorAllianceID': 673381830,
                        'id': 374119034},
            374133265: {'itemID': 1005888572647,
                        'payout': 1,
                        'amount': 5125528.4,
                        'id': 374133265}})

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/NotificationTexts', {'characterID': 1, 'IDs': 1234}),
            ])

    def test_standings(self):
        self.api.get.return_value = self.make_api_result("char/standings.xml")

        result, current, expires = self.char.standings()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
                'agents': {3009841: {'id': 3009841, 'name': 'Pausent Ansin', 'standing': 0.1},
                           3009846: {'id': 3009846, 'name': 'Charie Octienne', 'standing': 0.19}},
                'corps': {1000061: {'id': 1000061, 'name': 'Freedom Extension', 'standing': 0},
                          1000064: {'id': 1000064, 'name': 'Carthum Conglomerate', 'standing': 0.34},
                          1000094: {'id': 1000094, 'name': 'TransStellar Shipping', 'standing': 0.02}},
                'factions': {500003: {'id': 500003, 'name': 'Amarr Empire', 'standing': -0.1},
                             500020: {'id': 500020, 'name': 'Serpentis', 'standing': -1}}},
                )

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/Standings', {'characterID': 1}),
            ])

    def test_research(self):
        self.api.get.return_value = self.make_api_result("char/research.xml")

        result, current, expires = self.char.research()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

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

        result, current, expires = self.char.current_training()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

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

        result, current, expires = self.char.skill_queue()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

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

        result, current, expires = self.char.messages()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

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

    def test_message_bodies(self):
        self.api.get.return_value = self.make_api_result("char/message_bodies.xml")

        result, current, expires = self.char.message_bodies([297023723,297023208,297023210,297023211])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
                297023208: '<p>Another message</p>',
                297023210: None,
                297023211: None,
                297023723: 'Hi.<br><br>This is a message.<br><br>',
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/MailBodies', {
                    'characterID': 1,
                    'ids': [297023723,297023208,297023210,297023211],
                }),
            ])

    def test_mailing_lists(self):
        self.api.get.return_value = self.make_api_result("char/mailing_lists.xml")

        result, current, expires = self.char.mailing_lists()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
                128250439: "EVETycoonMail",
                128783669: "EveMarketScanner",
                141157801: "Exploration Wormholes",
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/MailingLists'),
            ])

    def test_calendar_events(self):
        self.api.get.return_value = self.make_api_result("char/calendar_events.xml")

        result, current, expires = self.char.calendar_events()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
                93264: {
                    'description': 'Join us for <a href="http://fanfest.eveonline.com/">     '
                                   'EVE Online\'s Fanfest 2011</a>!',
                    'duration': 0,
                    'id': 93264,
                    'important': False,
                    'owner': {
                        'id': 1,
                        'name': None,
                    },
                    'response': 'Undecided',
                    'start_ts': 1301130000,
                    'title': 'EVE Online Fanfest 2011',
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/UpcomingCalendarEvents', {
                    'characterID': 1,
                }),
            ])

    def test_calendar_attendees(self):
        self.api.get.return_value = self.make_api_result("char/calendar_attendees.xml")

        result, current, expires = self.char.calendar_attendees([123, 234, 345])
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
                123: {
                    123456789: {
                        'id': 123456789,
                        'name': 'Jane Doe',
                        'response': 'Accepted',
                    },
                    987654321: {
                        'id': 987654321,
                        'name': 'John Doe',
                        'response': 'Tentative',
                    },
                },
                234: {
                    192837645: {
                        'id': 192837645,
                        'name': 'Another Doe',
                        'response': 'Declined',
                    },
                    918273465: {
                        'id': 918273465,
                        'name': 'Doe the Third',
                        'response': 'Undecided',
                    },
                },
                345: {},
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/CalendarEventAttendees', {
                    'characterID': 1,
                    'eventIDs': [123, 234, 345],
                }),
            ])

    @mock.patch('evelink.char.Char.calendar_attendees')
    def test_event_attendees(self, mock_calendar):
        mock_calendar.return_value = evelink_api.APIResult(
            {42: mock.sentinel.attendees}, 12345, 67890)
        result, current, expires = self.char.event_attendees(42)
        self.assertEqual(result, mock.sentinel.attendees)
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

    def test_faction_warfare_stats(self):
        self.api.get.return_value = self.make_api_result("char/faction_warfare_stats.xml")

        result, current, expires = self.char.faction_warfare_stats()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
                'enlist_ts': 1213135800,
                'faction': {'id': 500001, 'name': 'Caldari State'},
                'kills': {'total': 0, 'week': 0, 'yesterday': 0},
                'points': {'total': 0, 'week': 1044, 'yesterday': 0},
                'rank': {'current': 4, 'highest': 4},
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/FacWarStats', {'characterID': 1}),
            ])

    def test_medals(self):
        self.api.get.return_value = self.make_api_result("char/medals.xml")

        result, current, expires = self.char.medals()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
                'current': {},
                'other': {
                    4106: {
                        'corp_id': 1711141370,
                        'description': 'For taking initiative and...',
                        'id': 4106,
                        'issuer_id': 132533870,
                        'public': False,
                        'reason': 'For continued support, loyalty...',
                        'title': 'Medal of Service'}}
            })

        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/Medals', {
                    'characterID': 1
                }),
            ])

    def test_contact_notifications(self):
        self.api.get.return_value = self.make_api_result("char/contact_notifications.xml")

        result, current, expires = self.char.contact_notifications()
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)

        self.assertEqual(result, {
                308734131: {
                    'data': {
                        'level': 10,
                        'message': 'Hi, I want to social network with you!',
                    },
                    'id': 308734131,
                    'sender': {
                        'id': 797400947,
                        'name': 'CCP Garthagk',
                    },
                    'timestamp': 1275174240,
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/ContactNotifications', {'characterID': 1}),
            ])

    def test_locations(self):
        self.api.get.return_value = self.make_api_result("char/locations.xml")

        result, current, expires = self.char.locations((1009661446486L, 1007448817800L))
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/Locations', {'characterID': 1, 'IDs': (1009661446486L, 1007448817800L),}),
            ])
        self.assertEqual(result,
            {1009661446486L:
                {
                    'id': 1009661446486L,
                    'x': None,
                    'z': None,
                    'name': "Superawesome test Impairor",
                    'y': None,
                },
            1007448817800L:
                {
                    'id': 1007448817800L,
                    'x': -170714848271.291,
                    'z': 208419106396.3,
                    'name': "A Whale",
                    'y': -1728060949.58229,
                }
            }
        )
        self.assertEqual(current, 12345)
        self.assertEqual(expires, 67890)


if __name__ == "__main__":
    unittest.main()
