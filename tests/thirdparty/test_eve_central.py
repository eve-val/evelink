import datetime
import os
from xml.etree import ElementTree

import mock
import unittest2 as unittest

import evelink.thirdparty.eve_central as evelink_evec

class EVECentralTestCase(unittest.TestCase):

    def test_item_orders(self):
        xml_file = os.path.join(os.path.dirname(__file__), '..',
            'xml', 'thirdparty', 'eve_central', 'item_orders.xml')
        url_fetch = mock.MagicMock()
        with open(xml_file) as f:
            url_fetch.return_value = f.read()

        evec = evelink_evec.EVECentral(url_fetch_func=url_fetch)

        results = evec.item_orders(1877)

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
                            'reported': datetime.datetime(2012, 9, 6, 22, 6, 36),
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
                            'reported': datetime.datetime(2012, 9, 6, 22, 6, 36),
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
        self.assertEqual(url_fetch.mock_calls, [
                mock.call('%s/quicklook?typeid=1877&sethours=360' % evec.api_base),
            ])

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

# vim: set et ts=4 sts=4 sw=4:
