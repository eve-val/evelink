
CONTACTS_MAP = {
    'allianceContactList': 'alliance',
    'corporateContactList': 'corp',
    'contactList': 'personal',
}

LABEL_MAP = {
    'contactLabels': 'personal',
    'corporateContactLabels': 'corp',
    'allianceContactLabels': 'alliance',
}


def parse_contact_list(api_result):
    result = {'labels': {}}
    for rowset in api_result.findall('rowset'):
        setname = rowset.get('name')

        if setname in CONTACTS_MAP:
            contact_list = result[CONTACTS_MAP[rowset.get('name')]] = {}
            for row in rowset.findall('row'):
                in_watchlist = (row.get('inWatchlist') == 'True'
                                if 'inWatchlist' in row.attrib
                                else None)
                contact_id = int(row.get('contactID'))
                contact_list[contact_id] = {
                    'id': contact_id,
                    'name': row.get('contactName'),
                    'standing': float(row.get('standing')),
                    'in_watchlist': in_watchlist,
                    'label_mask': int(row.get('labelMask') or 0),
                    'labels': {},
                }
        elif setname in LABEL_MAP:
            label_list = result['labels'][LABEL_MAP[setname]] = {}
            for row in rowset.findall('row'):
                label_id = int(row.get('labelID'))
                label_list[label_id] = {
                    'id': label_id,
                    'name': row.get('name'),
                }
    for grouping in ('personal', 'corp', 'alliance'):
        group = result.get(grouping)
        if not group:
            continue
        labels = result['labels'][grouping]
        for contact_id in group:
            contact = group[contact_id]
            labelMask = contact['label_mask']
            if labelMask:
                for label_id in labels:
                    if labelMask & label_id:
                        contact['labels'][label_id] = labels[label_id]
            del contact['label_mask']

    return result
