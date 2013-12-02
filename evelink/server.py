from evelink import api

class Server(object):
    """Wrapper around /server/ of the EVE API."""

    @api.auto_api
    def __init__(self, api=None):
        self.api = api

    @api.auto_call('server/ServerStatus')
    def server_status(self, api_result=None):
        """Check the current server status."""

        result = {
            'online': api.get_bool_value(api_result.result, 'serverOpen'),
            'players': api.get_int_value(api_result.result, 'onlinePlayers'),
        }

        return api.APIResult(result, api_result.timestamp, api_result.expires)

