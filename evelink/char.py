class Char(object):
    """Wrapper around /char/ of the EVE API.

    Note that a valid API key is required.
    """

    def __init__(self, api):
        self.api = api

    def wallet_info(self, character_id):
        """Return a given character's wallet."""
        api_result = self.api.get('char/AccountBalance',
            {'characterID': character_id})

        rowset = api_result.find('rowset')
        row = rowset.find('row')
        result = {
                'balance': float(row.attrib['balance']),
                'id': int(row.attrib['accountID']),
                'key': int(row.attrib['accountKey']),
            }
        return result

    def wallet_balance(self, character_id):
        """Helper to return just the balance from a given character wallet"""

        return self.wallet_info(character_id)['balance']

