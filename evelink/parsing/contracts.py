from evelink import api
from evelink import constants
import time

def parse_contracts(api_result):
    def parse_time(t):
        return time.strptime(t, '%Y-%m-%d %H:%M:%S')

    rowset = api_result.find('rowset')
    if rowset is None:
        return

    results = {}
    for row in rowset.findall('row'):
        contract = {
            'id': int(row.attrib['contractID']),
            'issuer': int(row.attrib['issuerID']),
            'issuer_corp': int(row.attrib['issuerCorpID']),
            'assignee': int(row.attrib['assigneeID']),
            'acceptor': int(row.attrib['acceptorID']),
            'start': int(row.attrib['startStationID']),
            'end': int(row.attrib['endStationID']),
            'type': row.attrib['type'],
            'status': row.attrib['status'],
            'corp': row.attrib['forCorp'] == '1',
            'availability': row.attrib['availability'],
            'issued': parse_time(row.attrib['dateIssued']),
            'days': int(row.attrib['numDays']),
            'price': float(row.attrib['price']),
            'reward': float(row.attrib['reward']),
            'collateral': float(row.attrib['collateral']),
            'buyout': float(row.attrib['buyout']),
            'volume': float(row.attrib['volume']),
            'title': row.attrib['title']
        }
        if row.attrib['dateExpired']:
            contract['expired'] = parse_time(row.attrib['dateExpired'])
        if row.attrib['dateAccepted']:
            contract['accepted'] = parse_time(row.attrib['dateAccepted'])
        if row.attrib['dateCompleted']:
            contract['completed'] = parse_time(row.attrib['dateCompleted'])
        results[contract['id']] = contract
    return results
