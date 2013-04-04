from evelink import api

def parse_wallet_transactions(api_result):
    rowset = api_result.find('rowset')
    rows = rowset.findall('row')
    result = []
    for row in rows:
        a = row.attrib
        entry = {
            'timestamp': api.parse_ts(a['transactionDateTime']),
            'id': int(a['transactionID']),
            'journal_id': int(a['journalTransactionID']),
            'quantity': int(a['quantity']),
            'type': {
                'id': int(a['typeID']),
                'name': a['typeName'],
            },
            'price': float(a['price']),
            'client': {
                'id': int(a['clientID']),
                'name': a['clientName'],
            },
            'station': {
                'id': int(a['stationID']),
                'name': a['stationName'],
            },
            'action': a['transactionType'],
            'for': a['transactionFor'],
        }
        if 'characterID' in a:
            entry['char'] = {
                'id': int(a['characterID']),
                'name': a['characterName'],
            }
        result.append(entry)

    return result
