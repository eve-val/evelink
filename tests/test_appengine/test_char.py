import mock

from tests.compat import unittest

from tests.test_appengine import (
    GAEAsyncTestCase
)

try:
    from evelink.appengine import AppEngineAPI
    from evelink.appengine.char import Char
except ImportError:
    Char = mock.Mock()


class AppEngineCharTestCase(GAEAsyncTestCase):
    
    def setUp(self):
        api = AppEngineAPI()
        self.client = Char(1, api)

    def test_assets_async(self):
        self.compare(
            Char,
            'assets',
            'corp/assets.xml',
            _client=self.client
        )
    
    def test_calendar_attendees_async(self):
        self.compare(
            Char,
            'calendar_attendees',
            'char/calendar_attendees.xml',
            [123,234,],
            _client=self.client
        )
    
    def test_calendar_events_async(self):
        self.compare(
            Char,
            'calendar_events',
            'char/calendar_events.xml',
            _client=self.client
        )
    
    def test_character_sheet_async(self):
        self.compare(
            Char,
            'character_sheet',
            'char/character_sheet.xml',
            _client=self.client
        )
    
    def test_contact_notifications_async(self):
        self.compare(
            Char,
            'contact_notifications',
            'char/contact_notifications.xml',
            _client=self.client
        )
    
    def test_contacts_async(self):
        self.compare(
            Char,
            'contacts',
            'char/contact_list.xml',
            _client=self.client
        )
    
    def test_contract_bids_async(self):
        self.compare(
            Char,
            'contract_bids',
            'char/contract_bids.xml',
            _client=self.client
        )
    
    def test_contract_items_async(self):
        self.compare(
            Char,
            'contract_items',
            'char/contract_items.xml',
            1228,
            _client=self.client
        )
    
    def test_contracts_async(self):
        self.compare(
            Char,
            'contracts',
            'corp/contracts.xml',
            _client=self.client
        )
    
    def test_current_training_async(self):
        self.compare(
            Char,
            'current_training',
            'char/current_training.xml',
            _client=self.client
        )
    
    def test_event_attendees_async(self):
        self.compare(
            Char,
            'event_attendees',
            'char/calendar_attendees_by_id.xml',
            234,
            _client=self.client
        )
    
    def test_faction_warfare_stats_async(self):
        self.compare(
            Char,
            'faction_warfare_stats',
            'char/faction_warfare_stats.xml',
            _client=self.client
        )
    
    def test_industry_jobs_async(self):
        self.compare(
            Char,
            'industry_jobs',
            'char/industry_jobs.xml',
            _client=self.client
        )
    
    def test_kills_async(self):
        self.compare(
            Char,
            'kills',
            'char/kills.xml',
            _client=self.client
        )
    
    def test_locations_async(self):
        self.compare(
            Char,
            'locations',
            'char/locations.xml',
            345678,
            _client=self.client
        )
    
    def test_mailing_lists_async(self):
        self.compare(
            Char,
            'mailing_lists',
            'char/mailing_lists.xml',
            _client=self.client
        )
    
    def test_medals_async(self):
        self.compare(
            Char,
            'medals',
            'char/medals.xml',
            _client=self.client
        )
    
    def test_message_bodies_async(self):
        self.compare(
            Char,
            'message_bodies',
            'char/message_bodies.xml',
            234567,
            _client=self.client
        )
    
    def test_messages_async(self):
        self.compare(
            Char,
            'messages',
            'char/messages.xml',
            _client=self.client
        )
    
    def test_notification_texts_async(self):
        self.compare(
            Char,
            'notification_texts',
            'char/notification_texts.xml',
            123456,
            _client=self.client
        )
    
    def test_notifications_async(self):
        self.compare(
            Char,
            'notifications',
            'char/notifications.xml',
            _client=self.client
        )
    
    def test_orders_async(self):
        self.compare(
            Char,
            'orders',
            'char/orders.xml',
            _client=self.client
        )
    
    def test_research_async(self):
        self.compare(
            Char,
            'research',
            'char/research.xml',
            _client=self.client
        )
    
    def test_skill_queue_async(self):
        self.compare(
            Char,
            'skill_queue',
            'char/skill_queue.xml',
            _client=self.client
        )
    
    def test_standings_async(self):
        self.compare(
            Char,
            'standings',
            'char/standings.xml',
            _client=self.client
        )
    
    def test_wallet_balance_async(self):
        self.compare(
            Char,
            'wallet_balance',
            'char/wallet_balance.xml',
            _client=self.client
        )
    
    def test_wallet_info_async(self):
        self.compare(
            Char,
            'wallet_info',
            'char/wallet_info.xml',
            _client=self.client
        )
    
    def test_wallet_journal_async(self):
        self.compare(
            Char,
            'wallet_journal',
            'char/wallet_journal.xml',
            _client=self.client
        )
    
    def test_wallet_transactions_async(self):
        self.compare(
            Char,
            'wallet_transactions',
            'char/wallet_transactions.xml',
            _client=self.client
        )


if __name__ == "__main__":
    unittest.main()
