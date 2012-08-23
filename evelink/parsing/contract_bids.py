from evelink import api

def parse_contract_bids(api_result):
    rowset = api_result.find('rowset')
    results = []
    for row in rowset.findall('row'):
        a = row.attrib

        bid = {
            'id': int(a['bidID']),
            'contract_id': int(a['contractID']),
            'bidder_id': int(a['bidderID']),
            'timestamp': api.parse_ts(a['dateBid']),
            'amount': float(a['amount']),
        }

        results.append(bid)

    return results


