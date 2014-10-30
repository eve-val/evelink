import datetime
import os
from xml.etree import ElementTree
import mock

from tests.compat import unittest

import evelink.thirdparty.eve_central as evelink_evec

class EVECentralTestCase(unittest.TestCase):

    def test_init(self):
        evec = evelink_evec.EVECentral()
        self.assertTrue(isinstance(evec, evelink_evec.EVECentral))

    @mock.patch('evelink.thirdparty.eve_central.EVECentral._parse_item_orders')
    def test_item_orders(self, mock_parse):
        url_fetch = mock.MagicMock()
        url_fetch.return_value = mock.sentinel.api_response
        mock_parse.return_value = mock.sentinel.parsed_results

        evec = evelink_evec.EVECentral(url_fetch_func=url_fetch)

        results = evec.item_orders(1877)

        self.assertEqual(results, mock.sentinel.parsed_results)
        self.assertEqual(url_fetch.mock_calls, [
                mock.call('%s/quicklook?typeid=1877&sethours=360' % evec.api_base),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_response),
            ])

    @mock.patch('evelink.thirdparty.eve_central.EVECentral._parse_item_orders')
    def test_item_orders_on_route(self, mock_parse):
        url_fetch = mock.MagicMock()
        url_fetch.return_value = mock.sentinel.api_response
        mock_parse.return_value = mock.sentinel.parsed_results

        evec = evelink_evec.EVECentral(url_fetch_func=url_fetch)

        results = evec.item_orders_on_route(1877, 'Jita', 'Amarr')

        self.assertEqual(results, mock.sentinel.parsed_results)
        self.assertEqual(url_fetch.mock_calls, [
                mock.call('%s/quicklook/onpath/from/Jita/to/Amarr/fortype/1877?sethours=360'
                    % evec.api_base),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.api_response),
            ])

    def test_parse_item_orders(self):
        xml_file = os.path.join(os.path.dirname(__file__), '..',
            'xml', 'thirdparty', 'eve_central', 'item_orders.xml')
        url_fetch = mock.MagicMock()
        with open(xml_file) as f:
            response = f.read()

        evec = evelink_evec.EVECentral(url_fetch_func=url_fetch)

        results = evec._parse_item_orders(response)

        this_year = datetime.datetime.now().year
        reported = datetime.datetime(this_year, 9, 6, 22, 6, 36)
        if reported > datetime.datetime.now():
            reported = reported.replace(year=this_year - 1)

        self.assertEqual(results, {
                'hours': 360,
                'id': 1877,
                'name': 'Rapid Light Missile Launcher II',
                'orders': {
                    'buy': {
                        2534467564: {
                            'expires': datetime.date(2012, 9, 14),
                            'id': 2534467564,
                            'price': 559000.0,
                            'range': 32767,
                            'region_id': 10000012,
                            'reported': reported,
                            'security': -0.0417728879761037,
                            'station': {
                                'id': 60012904,
                                'name': 'Litom XI - Moon 2 - Guardian Angels Assembly Plant',
                            },
                            'volume': {'minimum': 1, 'remaining': 12},
                        }
                    },
                    'sell': {
                        2534467565: {
                            'expires': datetime.date(2012, 9, 14),
                            'id': 2534467565,
                            'price': 559000.0,
                            'range': 32767,
                            'region_id': 10000012,
                            'reported': reported,
                            'security': -0.0417728879761037,
                            'station': {
                                'id': 60012904,
                                'name': 'Litom XI - Moon 2 - Guardian Angels Assembly Plant',
                            },
                            'volume': {'minimum': 1, 'remaining': 12},
                        },
                    },
                },
                'quantity_min': 1,
                'regions': ['Curse'],
            })

    def test_market_stats(self):
        xml_file = os.path.join(os.path.dirname(__file__), '..',
            'xml', 'thirdparty', 'eve_central', 'market_stats.xml')
        url_fetch = mock.MagicMock()
        with open(xml_file) as f:
            url_fetch.return_value = f.read()

        evec = evelink_evec.EVECentral(url_fetch_func=url_fetch)

        results = evec.market_stats([34])

        self.assertEqual(results, {
                34: {
                    'id': 34,
                    'all': {
                        'avg': 6.56,
                        'max': 14.0,
                        'median': 6.14,
                        'min': 0.18,
                        'percentile': 4.18,
                        'stddev': 1.41,
                        'volume': 46077525904,
                    },
                    'buy': {
                        'avg': 5.78,
                        'max': 6.14,
                        'median': 6.0,
                        'min': 2.46,
                        'percentile': 6.14,
                        'stddev': 0.99,
                        'volume': 22770318895,
                    },
                    'sell': {
                        'avg': 7.43,
                        'max': 20.0,
                        'median': 6.64,
                        'min': 5.79,
                        'percentile': 6.15,
                        'stddev': 1.69,
                        'volume': 22944882136,
                    },
                },
            })
        self.assertEqual(url_fetch.mock_calls, [
                mock.call('%s/marketstat?typeid=34&hours=24' % evec.api_base),
            ])

    @mock.patch('evelink.thirdparty.eve_central.EVECentral.market_stats')
    def test_item_market_stats(self, mock_stats):
        mock_stats.return_value = {123:mock.sentinel.stats_retval}
        mock_fetch = mock.MagicMock()

        evec = evelink_evec.EVECentral(url_fetch_func=mock_fetch)

        result = evec.item_market_stats(123)

        self.assertEqual(result, mock.sentinel.stats_retval)
        self.assertEqual(mock_fetch.mock_calls, [])
        self.assertEqual(mock_stats.mock_calls, [
                mock.call([123]),
            ])

    def test_route(self):
        mock_fetch = mock.MagicMock()
        mock_fetch.return_value = """
                [{"fromid":1,"from":"Test","toid":2,"to":"Testing","secchange":false}]
            """.strip()

        evec = evelink_evec.EVECentral(url_fetch_func=mock_fetch)

        results = evec.route('Test', 2)

        self.assertEqual(results, [
                {
                    'from': {'id': 1, 'name': 'Test'},
                    'to': {'id': 2, 'name': 'Testing'},
                    'security_change': False,
                },
            ])
        self.assertEqual(mock_fetch.mock_calls, [
                mock.call('%s/route/from/Test/to/2' % evec.api_base),
            ])



# vim: set et ts=4 sts=4 sw=4:
