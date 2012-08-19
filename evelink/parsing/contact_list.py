
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
            in_watchlist = (row.get('inWatchlist') == 'True'
                            if 'inWatchlist' in row.attrib
                            else None)
            contact_id = int(row.get('contactID'))
            contact_list[contact_id] = {
                'id': contact_id,
                'name': row.get('contactName'),
                'standing': float(row.get('standing')),
                'in_watchlist': in_watchlist
            }

    return result
        
