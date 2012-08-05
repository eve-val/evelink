from evelink import api
from evelink import constants
import time

def parse_contracts(api_result):
    rowset = api_result.find('rowset')
    if rowset is None:
        return

    results = {}
    for row in rowset.findall('row'):
        a = row.attrib
        contract = {
            'id': int(a['contractID']),
            'issuer': int(a['issuerID']),
            'issuer_corp': int(a['issuerCorpID']),
            'assignee': int(a['assigneeID']),
            'acceptor': int(a['acceptorID']),
            'start': int(a['startStationID']),
            'end': int(a['endStationID']),
            'type': a['type'],
            'status': a['status'],
            'corp': a['forCorp'] == '1',
            'availability': a['availability'],
            'issued': api.parse_ts(a['dateIssued']),
            'days': int(a['numDays']),
            'price': float(a['price']),
            'reward': float(a['reward']),
            'collateral': float(a['collateral']),
            'buyout': float(a['buyout']),
            'volume': float(a['volume']),
            'title': a['title']
        }
        contract['expired'] = api.parse_ts(a['dateExpired'])
        contract['accepted'] = api.parse_ts(a['dateAccepted'])
        contract['completed'] = api.parse_ts(a['dateCompleted'])
        results[contract['id']] = contract
    return results
