from evelink import api
from evelink import constants

def parse_market_orders(api_result):
        rowset = api_result.find('rowset')
        rows = rowset.findall('row')
        result = {}
        for row in rows:
            a = row.attrib
            id = int(a['orderID'])
            result[id] = {
                'id': id,
                'char_id': int(a['charID']),
                'station_id': int(a['stationID']),
                'amount': int(a['volEntered']),
                'amount_left': int(a['volRemaining']),
                'status': constants.Market().order_status[int(a['orderState'])],
                'type_id': int(a['typeID']),
                'range': int(a['range']),
                'account_key': int(a['accountKey']),
                'duration': int(a['duration']),
                'escrow': float(a['escrow']),
                'price': float(a['price']),
                'type': 'buy' if a['bid'] == '1' else 'sell',
                'timestamp': api.parse_ts(a['issued']),
            }

        return result
