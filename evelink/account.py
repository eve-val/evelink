from evelink import api

class Account(object):
    """Wrapper around /account/ of the EVE API.

    Note that a valid API key is required.
    """

    def __init__(self, api):
        self.api = api

    def status(self):
        """Returns the account's subscription status."""
        api_result = self.api.get('account/AccountStatus')

        _str, _int, _float, _bool, _ts = api.elem_getters(api_result)

        return {
            'paid_ts': _ts('paidUntil'),
            'create_ts': _ts('createDate'),
            'logins': _int('logonCount'),
            'minutes_played': _int('logonMinutes'),
        }
