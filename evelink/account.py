from evelink import api
from evelink import constants

class Account(object):
    """Wrapper around /account/ of the EVE API.

    Note that a valid API key is required.
    """

    def __init__(self, api):
        self.api = api

    @api.auto_call('account/AccountStatus')
    def status(self, api_result=None):
        """Returns the account's subscription status."""
        _str, _int, _float, _bool, _ts = api.elem_getters(api_result.result)

        result = {
            'paid_ts': _ts('paidUntil'),
            'create_ts': _ts('createDate'),
            'logins': _int('logonCount'),
            'minutes_played': _int('logonMinutes'),
        }

        rowsets = dict((r.attrib['name'], r) for r in api_result.result.findall('rowset'))

        result['multi_training_ends'] = [
            api.parse_ts(m.attrib['trainingEnd'])
            for m in rowsets['multiCharacterTraining']]

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @api.auto_call('account/APIKeyInfo')
    def key_info(self, api_result=None):
        """Returns the details of the API key being used to auth."""
        key = api_result.result.find('key')
        result = {
            'access_mask': int(key.attrib['accessMask']),
            'type': constants.APIKey.key_types[key.attrib['type']],
            'expire_ts': api.parse_ts(key.attrib['expires']) if key.attrib['expires'] else None,
            'characters': {},
        }

        rowset = key.find('rowset')
        for row in rowset.findall('row'):
            character = {
                'id': int(row.attrib['characterID']),
                'name': row.attrib['characterName'],
                'corp': {
                    'id': int(row.attrib['corporationID']),
                    'name': row.attrib['corporationName'],
                },
            }
            if 'allianceID' in row.attrib:
                character['alliance'] = {
                    'id': int(row.attrib['allianceID']),
                    'name': row.attrib['allianceName'],
                }
            else:
                character['alliance'] = None
            result['characters'][character['id']] = character

        return api.APIResult(result, api_result.timestamp, api_result.expires)

    @api.auto_call('account/Characters')
    def characters(self, api_result=None):
        """Returns all of the characters on an account."""
        rowset = api_result.result.find('rowset')
        result = {}
        for row in rowset.findall('row'):
            character = {
                'id': int(row.attrib['characterID']),
                'name': row.attrib['name'],
                'corp': {
                    'id': int(row.attrib['corporationID']),
                    'name': row.attrib['corporationName'],
                },
            }
            if 'allianceID' in row.attrib:
                character['alliance'] = {
                    'id': int(row.attrib['allianceID']),
                    'name': row.attrib['allianceName'],
                }
            else:
                character['alliance'] = None
            result[character['id']] = character

        return api.APIResult(result, api_result.timestamp, api_result.expires)
