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

    @mock.patch('evelink.char.parse_contract_bids')
    def test_contract_bids(self, mock_parse):
        self.api.get.return_value = mock.sentinel.contract_bids_api_result
        mock_parse.return_value = mock.sentinel.parsed_contract_bids

        result = self.char.contract_bids()
        self.assertEqual(result, mock.sentinel.parsed_contract_bids)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.contract_bids_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/ContractBids', {'characterID': 1}),
            ])

    @mock.patch('evelink.char.parse_contract_items')
    def test_contract_items(self, mock_parse):
        self.api.get.return_value = mock.sentinel.contract_items_api_result
        mock_parse.return_value = mock.sentinel.parsed_contract_items

        result = self.char.contract_items(12345)
        self.assertEqual(result, mock.sentinel.parsed_contract_items)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.contract_items_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/ContractItems', {'characterID': 1, 'contractID': 12345}),
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

    @mock.patch('evelink.char.parse_wallet_journal')
    def test_wallet_journal(self, mock_parse):
        self.api.get.return_value = mock.sentinel.journal_api_result
        mock_parse.return_value = mock.sentinel.parsed_journal

        result = self.char.wallet_journal()
        self.assertEqual(result, mock.sentinel.parsed_journal)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.journal_api_result),
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

    @mock.patch('evelink.char.parse_wallet_transactions')
    def test_wallet_transcations(self, mock_parse):
        self.api.get.return_value = mock.sentinel.transactions_api_result
        mock_parse.return_value = mock.sentinel.parsed_transactions

        result = self.char.wallet_transactions()
        self.assertEqual(result, mock.sentinel.parsed_transactions)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.transactions_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/WalletTransactions', {'characterID': 1}),
            ])

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

    @mock.patch('evelink.char.parse_kills')
    def test_kills(self, mock_parse):
        self.api.get.return_value = mock.sentinel.kills_api_result
        mock_parse.return_value = mock.sentinel.kills

        result = self.char.kills()

        self.assertEqual(result, mock.sentinel.kills)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/KillLog', {'characterID': 1}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.kills_api_result),
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
        self.api.get.return_value = mock.sentinel.contacts_api_result
        mock_parse.return_value = mock.sentinel.parsed_contacts

        result = self.char.contacts()
        self.assertEqual(result, mock.sentinel.parsed_contacts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.contacts_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('char/ContactList', {'characterID': 1}),
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

    def test_standings(self):
        self.api.get.return_value = self.make_api_result("char/standings.xml")

        result = self.char.standings()

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

    def test_message_bodies(self):
        self.api.get.return_value = self.make_api_result("char/message_bodies.xml")

        result = self.char.message_bodies([297023723,297023208,297023210,297023211])

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

        result = self.char.mailing_lists()

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

        result = self.char.calendar_events()

        self.assertEqual(result, {
                93264: {
                    'description': 'Join us for <a href="http://fanfest.eveonline.com/">     EVE Online\'s Fanfest 2011</a>!',
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

        result = self.char.calendar_attendees([123, 234, 345])

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
        mock_calendar.return_value = {42: mock.sentinel.attendees}
        result = self.char.event_attendees(42)
        self.assertEqual(result, mock.sentinel.attendees)


if __name__ == "__main__":
    unittest.main()
