def parse_assets(api_result):
    def handle_rowset(rowset, parent_location):
        results = []
        for row in rowset.findall('row'):
            item = {'id': int(row.attrib['itemID']),
                    'item_type_id': int(row.attrib['typeID']),
                    'location_id': int(row.attrib.get('locationID', parent_location)),
                    'location_flag': int(row.attrib['flag']),
                    'quantity': int(row.attrib['quantity']),
                    'packaged': row.attrib['singleton'] == '0',
            }
            raw_quantity = row.attrib.get('rawQuantity')
            if raw_quantity is not None:
                item['raw_quantity'] = int(raw_quantity)
            contents = row.find('rowset')
            if contents is not None:
                item['contents'] = handle_rowset(contents, item['location_id'])
            results.append(item)
        return results

    result_list = handle_rowset(api_result.find('rowset'), None)
    # For convenience, key the result by top-level location ID.
    result_dict = {}
    for item in result_list:
        location = item['location_id']
        result_dict.setdefault(location, {})
        result_dict[location]['location_id'] = location
        result_dict[location].setdefault('contents', [])
        result_dict[location]['contents'].append(item)
    return result_dict
