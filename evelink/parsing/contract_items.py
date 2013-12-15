def parse_contract_items(api_result):
    rowset = api_result.find('rowset')
    results = []
    for row in rowset.findall('row'):
        a = row.attrib
        item = {
            'id': int(a['recordID']),
            'type_id': int(a['typeID']),
            'quantity': int(a['quantity']),
            'singleton': a['singleton'] == '1',
            'action': 'offered' if a['included'] == '1' else 'requested',
        }
        if 'rawQuantity' in a:
          item['raw_quantity'] = int(a['rawQuantity'])

        results.append(item)

    return results

