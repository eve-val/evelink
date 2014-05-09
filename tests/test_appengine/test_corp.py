import mock

from tests.compat import unittest

from tests.test_appengine import (
    GAEAsyncTestCase, auto_test_async_method
)

try:
    from evelink.appengine.corp import Corp
except ImportError:
    Corp = mock.Mock()

@auto_test_async_method(
    Corp, 
    (
        # 'kills',
        'permissions_log',
        # 'starbase_details',
        # 'industry_jobs',
        # 'locations',
        'faction_warfare_stats',
        'titles',
        'members',
        # 'station_services',
        # 'wallet_transactions',
        'corporation_sheet',
        # 'contract_bids',
        # 'orders',
        'permissions',
        'wallet_info',
        'shareholders',
        'container_log',
        'assets',
        # 'contacts',
        'stations',
        'member_medals',
        # 'contract_items',
        'npc_standings',
        'contracts',
        'wallet_journal',
        'medals',
        'starbases',
    )
)
class AppEngineCorpTestCase(GAEAsyncTestCase):
    
    def test_wallet_transactions_async(self):
        self.compare(
            Corp,
            'wallet_transactions',
            "char/wallet_transactions.xml"
        )

    def test_station_services_async(self):
        self.compare(
            Corp,
            'station_services',
            "corp/station_services.xml",
            61000368
        )

    def test_starbase_details_async(self):
        self.compare(
            Corp,
            'starbase_details',
            "corp/starbase_details.xml",
            1234
        )

    def test_orders_async(self):
        self.compare(
            Corp,
            'orders',
            "char/orders.xml",
        )

    def test_locations_async(self):
        self.compare(
            Corp,
            'locations',
            "corp/locations.xml",
            1234
        )

    def test_kills_async(self):
        self.compare(
            Corp,
            'kills',
            "char/kills.xml",
        )
    
    def test_industry_jobs_async(self):
        self.compare(
            Corp,
            'industry_jobs',
            "char/industry_jobs.xml",
        )

    def test_contract_items_async(self):
        self.compare(
            Corp,
            'contract_items',
            "char/contract_items.xml",
            1234
        )

    def test_contract_bids_async(self):
        self.compare(
            Corp,
            'contract_bids',
            "char/contract_bids.xml",
        )

    def test_contacts_async(self):
        self.compare(
            Corp,
            'contacts',
            "char/contact_list.xml",
        )


if __name__ == "__main__":
    unittest.main()
