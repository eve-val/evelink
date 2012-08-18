import mock
import unittest2 as unittest

import evelink.corp as evelink_corp
from tests.utils import APITestCase

class CorpTestCase(APITestCase):

    def setUp(self):
        super(CorpTestCase, self).setUp()
        self.corp = evelink_corp.Corp(api=self.api)

    @mock.patch('evelink.corp.parse_industry_jobs')
    def test_industry_jobs(self, mock_parse):
        self.api.get.return_value = mock.sentinel.industry_jobs_api_result
        mock_parse.return_value = mock.sentinel.industry_jobs

        result = self.corp.industry_jobs()

        self.assertEqual(result, mock.sentinel.industry_jobs)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/IndustryJobs'),
            ]) 
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.industry_jobs_api_result),
            ])

    @mock.patch('evelink.corp.parse_contracts')
    def test_contracts(self, mock_parse):
        self.api.get.return_value = mock.sentinel.contracts_api_result
        mock_parse.return_value = mock.sentinel.parsed_contracts

        result = self.corp.contracts()
        self.assertEqual(result, mock.sentinel.parsed_contracts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.contracts_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Contracts'),
            ])


    def test_wallet_info(self):
        self.api.get.return_value = self.make_api_result("corp/wallet_info.xml")

        result = self.corp.wallet_info()

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
                mock.call.get('corp/AccountBalance'),
            ])

    @mock.patch('evelink.corp.parse_market_orders')
    def test_orders(self, mock_parse):
        self.api.get.return_value = mock.sentinel.orders_api_result
        mock_parse.return_value = mock.sentinel.parsed_orders

        result = self.corp.orders()
        self.assertEqual(result, mock.sentinel.parsed_orders)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.orders_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MarketOrders'),
            ])

    @mock.patch('evelink.corp.parse_assets')
    def test_assets(self, mock_parse):
        self.api.get.return_value = mock.sentinel.assets_api_result
        mock_parse.return_value = mock.sentinel.parsed_assets

        result = self.corp.assets()
        self.assertEqual(result, mock.sentinel.parsed_assets)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.assets_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/AssetList'),
            ])

if __name__ == "__main__":
    unittest.main()
