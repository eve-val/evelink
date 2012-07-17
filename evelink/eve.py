from evelink import api

class EVE(object):
    """Wrapper around /eve/ of the EVE API."""

    @api.auto_api
    def __init__(self, api=None):
        self.api = api

    def character_ids_from_names(self, name_list):
        """Retrieve a dict mapping character names to IDs.

        name_list:
            A list of names to retrieve character IDs.

        Names of unknown characters will map to None.
        """

        api_result = self.api.get('eve/CharacterID', {
                'names': name_list,
            })

        rowset = api_result.find('rowset')
        rows = rowset.findall('row')

        results = {}
        for row in rows:
            name = row.attrib['name']
            char_id = int(row.attrib['characterID']) or None
            results[name] = char_id

        return results

    def character_id_from_name(self, name):
        """Retrieve the named character's ID.

        Convenience wrapper around character_ids().
        """
        return self.character_ids_from_names([name]).get(name)

    def character_info_from_id(self, char_id):
        """Retrieve a dict of info about the designated character."""

        api_result = self.api.get('eve/CharacterInfo', {
                'characterID': char_id,
            })

        def _str(key): return api.get_named_value(api_result, key)
        def _int(key): return api.get_int_value(api_result, key)
        def _float(key): return float(_str(key))
        def _ts(key): return api.get_ts_value(api_result, key)

        results = {
            'id': _int('characterID'),
            'name': _str('characterName'),
            'race': _str('race'),
            'bloodline': _str('bloodline'),
            'corp_id': _int('corporationID'),
            'corp_name': _str('corporation'),
            'corp_ts': _ts('corporationDate'),
            'sec_status': _float('securityStatus'),
            'history': [],
        }

        # Add in corp history
        history = api_result.find('rowset')
        for row in history.findall('row'):
            corp_id = row.attrib['corporationID']
            start_date = api.parse_ts(row.attrib['startDate'])
            results['history'].append({
                    'corp_id': corp_id,
                    'start_ts': start_date,
                })

        return results
