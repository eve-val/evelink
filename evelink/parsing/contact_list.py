
LABEL_MAP = {
    'allianceContactList': 'alliance',
    'corporateContactList': 'corp',
    'contactList': 'personal',
}
def parse_contact_list(api_result):
    result = {}
    for rowset in api_result.findall('rowset'):
        contact_list = result[LABEL_MAP[rowset.get('name')]] = {}
        for row in rowset.findall('row'):
            d = {
                'id': int(row.get('contactID')),
                'name': row.get('contactName'),
                'standing': float(row.get('standing')),
            }
            if 'inWatchlist' in row.attrib:
                d['in_watchlist'] = row.get('inWatchlist', 'False') == 'True'
            contact_list[d['id']] = d

    return result
        
