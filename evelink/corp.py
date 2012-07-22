from evelink.parsing.industry_jobs import parse_industry_jobs

class Corp(object):
    """Wrapper around /corp/ of the EVE API.

    Note that a valid corp API key is required.
    """

    def __init__(self, api):
        self.api = api

    def industry_jobs(self):
        """Get a list of jobs for a corporation."""

        api_result = self.api.get('corp/IndustryJobs')

        return parse_industry_jobs(api_result)

    def wallet_info(self):
        """Get information about corp wallets."""

        api_result = self.api.get('corp/AccountBalance')

        rowset = api_result.find('rowset')
        results = {}
        for row in rowset.findall('row'):
            wallet = {
                'balance': float(row.attrib['balance']),
                'id': int(row.attrib['accountID']),
                'key': int(row.attrib['accountKey']),
            }
            results[wallet['key']] = wallet

        return results

    def assets(self):
        """Get information about corp assets.

        Each item is a dict, with keys 'id', 'item_type', 'quantity',
        'location', 'flag', and 'packaged'.  'Flag' denotes additional
        information about the item's location; see
        http://wiki.eve-id.net/API_Inventory_Flags for more details.

        If the item corresponds to a container, it will have a key
        'contents', which is itself a list of items in the same format
        (potentially recursively holding containers of its own).  If
        the contents do not have 'location' IDs of their own, they
        inherit the 'location' ID of their parent container, for
        convenience.

        At the top level, the result is a dict mapping location ID
        (typically a solar system) to a dict containing a 'contents'
        key, which maps to a list of items.  That is, you can think of
        the top-level values as "containers" with no fields except for
        "contents" and "location".
        """
        api_result = self.api.get('corp/AssetList')

        def handle_rowset(rowset, parent_location):
            results = []
            for row in rowset.findall('row'):
                item = {}
                item['id'] = int(row.attrib['itemID'])
                item['item_type'] = int(row.attrib['typeID'])
                item['quantity'] = int(row.attrib['quantity'])
                item['location'] = int(
                    row.attrib.get('locationID', parent_location))
                item['flag'] = int(row.attrib['flag'])
                item['packaged'] = not bool(int(row.attrib['singleton']))
                if not item['packaged']:
                    assert item['quantity'] == 1
                assert(len(row.findall('rowset')) <= 1)
                contents = row.find('rowset')
                if contents:
                    item['contents'] = handle_rowset(contents, item['location'])
                results.append(item)
            return results

        result_list = handle_rowset(api_result.find('rowset'), None)
        # For convenience, key the result by top-level location ID.
        result_dict = {}
        for item in result_list:
            location = item['location']
            result_dict.setdefault(location, {})
            result_dict[location]['location'] = location
            result_dict[location].setdefault('contents', [])
            result_dict[location]['contents'].append(item)
        return result_dict
