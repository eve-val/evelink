import datetime
import json
import urllib
from xml.etree import ElementTree

try:
    import urllib2
except ImportError:
    urllib2 = None

class EVECentral(object):

    def __init__(self, url_fetch_func=None,
        api_base='http://api.eve-central.com/api'):
        super(EVECentral, self).__init__()

        self.api_base = api_base

        if url_fetch_func is not None:
            self.url_fetch = url_fetch_func
        elif urllib2 is not None:
            self.url_fetch = self._default_fetch_func
        else:
            raise ValueError("urllib2 not available - specify url_fetch_func")

    def _default_fetch_func(self, url):
        """Fetches a given URL using GET and returns the response."""
        return urllib2.urlopen(url).read()

    def market_stats(self, type_ids, hours=24, regions=None, system=None,
        quantity_threshold=None):
        """Fetches market statistics for one or more items.

        Optional filters:
            hours (int) - Time period to compute statistics for.
            regions (list of ints) - Region id(s) for which to compute stats.
            systems (int) - System id for which to compute stats.
            quantity_threshold (int) - minimum size of order to consider.
        """

        params = [('typeid', type_ids), ('hours', hours)]
        if regions:
            params.append(('regionlimit', regions))
        if system:
            params.append(('usesystem', system))
        if quantity_threshold:
            params.append(('minQ', quantity_threshold))

        query = urllib.urlencode(params, True)
        url = '%s/marketstat?%s' % (self.api_base, query)

        response = self.url_fetch(url)
        api_result = ElementTree.fromstring(response)

        results = {}
        stats = api_result.find('marketstat')
        for type_section in stats.findall('type'):
            type_id = int(type_section.attrib['id'])
            type_result = {'id': type_id}
            for sub in ('all', 'buy', 'sell'):
                s = type_section.find(sub)
                sub_result = {
                    'volume': int(s.find('volume').text),
                    'avg': float(s.find('avg').text),
                    'max': float(s.find('max').text),
                    'min': float(s.find('min').text),
                    'stddev': float(s.find('stddev').text),
                    'median': float(s.find('median').text),
                    'percentile': float(s.find('percentile').text),
                }
                type_result[sub] = sub_result
            results[type_id] = type_result

        return results

    def item_market_stats(self, type_id, *args, **kwargs):
        """Fetch market statistics for a single item.

        (Convenience wrapper for market_stats.)
        """
        return self.market_stats([type_id], *args, **kwargs)[int(type_id)]

    def item_orders(self, type_id, hours=360, regions=None, system=None,
        quantity_threshold=None):
        """Fetches market orders for a given item.

        Optional filters:
            hours (int) - The time period from which to fetch posted orders.
            regions (list of ints) - Region id(s) for which to fetch orders.
            systems (int) - System id for which to fetch orders.
            quantity_threshold (int) - minimum size of order to consider.
        """

        params = [('typeid', type_id), ('sethours', hours)]
        if regions:
            params.append(('regionlimit', regions))
        if system:
            params.append(('usesystem', system))
        if quantity_threshold:
            params.append(('setminQ', quantity_threshold))

        query = urllib.urlencode(params, True)
        url = '%s/quicklook?%s' % (self.api_base, query)

        response = self.url_fetch(url)
        return self._parse_item_orders(response)

    def item_orders_on_route(self, type_id, start, dest, hours=360,
        quantity_threshold=None):
        """Fetches market orders for a given item along a shortest-path route.

        Optional filters:
            hours (int) - The time period from which to fetch posted orders.
            quantity_threshold (int) - minimum size of order to consider.
        """

        params = [('sethours', hours)]
        if quantity_threshold:
            params.append(('setminQ', quantity_threshold))

        query = urllib.urlencode(params, True)
        url = '%s/quicklook/onpath/from/%s/to/%s/fortype/%s?%s' % (
            self.api_base, start, dest, type_id, query)

        response = self.url_fetch(url)
        return self._parse_item_orders(response)

    def _parse_item_orders(self, response):
        """Shared parsing functionality for market order data from EVE-Central."""
        api_result = ElementTree.fromstring(response)

        res = api_result.find('quicklook')
        regions = res.find('regions').findall('region')
        results = {
            'id': int(res.find('item').text),
            'name': res.find('itemname').text,
            'hours': int(res.find('hours').text),
            'quantity_min': int(res.find('minqty').text),
            'regions': [r.text for r in regions] or None,
            'orders': {},
        }

        for act in ('buy', 'sell'):
            sub_result = {}
            for order in res.find('%s_orders' % act).findall('order'):
                order_id = int(order.attrib['id'])
                o = {
                    'id': order_id,
                    'region_id': int(order.find('region').text),
                    'station': {
                        'id': int(order.find('station').text),
                        'name': order.find('station_name').text,
                    },
                    'security': float(order.find('security').text),
                    'range': int(order.find('range').text),
                    'price': float(order.find('price').text),
                    'volume': {
                        'remaining': int(order.find('vol_remain').text),
                        'minimum': int(order.find('min_volume').text),
                    },
                    'expires': datetime.datetime.strptime(
                        order.find('expires').text,
                        "%Y-%m-%d",
                    ).date(),
                    'reported': datetime.datetime.strptime(
                        order.find('reported_time').text,
                        "%m-%d %H:%M:%S",
                    ),
                }

                # Correct errors due to EVE-Central only reporting the month
                # and day of the report, not the year. (Assumes reports are
                # never from the future and never older than a year.)
                this_year = datetime.datetime.now().year
                o['reported'] = o['reported'].replace(year=this_year)
                if o['reported'] > datetime.datetime.now():
                    previous_year = o['reported'].year - 1
                    o['reported'] = o['reported'].replace(year=previous_year)

                sub_result[order_id] = o

            results['orders'][act] = sub_result

        return results

    def route(self, start, dest):
        """Returns a shortest-path route between two systems.

        Both start and dest can be either exact system names or
        system IDs.
        """

        url = '%s/route/from/%s/to/%s' % (self.api_base, start, dest)
        response = self.url_fetch(url)

        stops = json.loads(response)

        results = []
        for stop in stops:
            results.append({
                'from': {
                    'id': stop['fromid'],
                    'name': stop['from'],
                },
                'to': {
                    'id': stop['toid'],
                    'name': stop['to'],
                },
                'security_change': stop['secchange'],
            })

        return results



# vim: set et ts=4 sts=4 sw=4:
