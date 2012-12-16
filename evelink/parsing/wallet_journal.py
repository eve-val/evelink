from evelink import api

def parse_wallet_journal(api_result):
    rowset = api_result.find('rowset')
    result = []

    for row in rowset.findall('row'):
        a = row.attrib
        entry = {
            'timestamp': api.parse_ts(a['date']),
            'id': int(a['refID']),
            'type_id': int(a['refTypeID']),
            'party_1': {
                'name': a['ownerName1'],
                'id': int(a['ownerID1']),
            },
            'party_2': {
                'name': a['ownerName2'],
                'id': int(a['ownerID2']),
            },
            'arg': {
                'name': a['argName1'],
                'id': int(a['argID1']),
            },
            'amount': float(a['amount']),
            'balance': float(a['balance']),
            'reason': a['reason'],
            # The tax fields might be an empty string, or not present
            # at all (e.g., for corp wallet records.)  Need to handle
            # both edge cases.
            'tax': {
                'taxer_id': int(a.get('taxReceiverID') or 0),
                'amount': float(a.get('taxAmount') or 0),
            },
        }

        result.append(entry)

    result.sort(key=lambda x: x['id'])
    return result


